"""
Summarizer Agent
Generates concise summaries of earnings call transcripts.
"""

from typing import Dict, Any
from agents.base_agent import BaseAgent


class SummarizerAgent(BaseAgent):
    """
    Summarizes earnings call transcripts into key points.
    
    Extracts:
    - Executive summary
    - Key financial metrics
    - Strategic initiatives
    - Guidance and outlook
    """
    
    def __init__(self, model=None, config=None):
        super().__init__("Summarizer", model, config)
        self.max_summary_length = config.get("max_summary_length", 500) if config else 500
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate transcript input."""
        if not input_data:
            self.logger.error("Empty input")
            return False
        
        if isinstance(input_data, dict):
            if "transcript" not in input_data:
                self.logger.error("Missing 'transcript' key")
                return False
            input_data = input_data["transcript"]
        
        if not isinstance(input_data, str):
            self.logger.error("Transcript must be string")
            return False
        
        if len(input_data) < 100:
            self.logger.error("Transcript too short")
            return False
        
        return True
    
    def analyze(self, input_data: Any) -> Dict[str, Any]:
        """Generate summary of the transcript."""
        
        # Extract transcript text
        if isinstance(input_data, dict):
            transcript = input_data["transcript"]
            company = input_data.get("company", "Unknown")
            quarter = input_data.get("quarter", "Unknown")
            year = input_data.get("year", "Unknown")
        else:
            transcript = input_data
            company = "Unknown"
            quarter = "Unknown"
            year = "Unknown"
        
        self.logger.info(f"Summarizing {len(transcript)} characters")
        
        # Create prompt for LLM
        prompt = f"""Analyze this earnings call transcript and provide a structured summary.

Transcript:
{transcript[:4000]}  

Please provide:
1. EXECUTIVE SUMMARY (2-3 sentences)
2. KEY FINANCIAL METRICS (revenue, earnings, margins, etc.)
3. STRATEGIC INITIATIVES (new products, partnerships, changes)
4. GUIDANCE & OUTLOOK (future expectations)
5. MANAGEMENT TONE (confident, cautious, optimistic, etc.)

Format as clear sections with bullet points."""
        
        # Generate summary using LLM or API
        if self.model:
            summary = self._generate_with_model(prompt)
        else:
            summary = self._generate_with_api(prompt)
        
        # Parse the summary into structured format
        structured_summary = self._structure_summary(summary)
        
        return {
            "company": company,
            "quarter": quarter,
            "year": year,
            "raw_summary": summary,
            "structured_summary": structured_summary,
            "transcript_length": len(transcript),
            "summary_length": len(summary)
        }
    
    def _generate_with_model(self, prompt: str) -> str:
        """Generate summary using local model."""
        try:
            from transformers import AutoTokenizer
            
            tokenizer = AutoTokenizer.from_pretrained("trained_model/final")
            inputs = tokenizer(prompt, return_tensors="pt", max_length=2048, truncation=True)
            
            with __import__('torch').no_grad():
                outputs = self.model.generate(
                    **inputs.to(self.model.device),
                    max_new_tokens=500,
                    temperature=0.7,
                    do_sample=True
                )
            
            summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Remove the prompt from output
            summary = summary[len(prompt):].strip()
            return summary
            
        except Exception as e:
            self.logger.error(f"Model generation failed: {e}")
            return self._generate_extractive_summary(prompt)
    
    def _generate_with_api(self, prompt: str) -> str:
        """Generate summary using Claude API."""
        try:
            import anthropic
            import os
            
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
            
        except Exception as e:
            self.logger.warning(f"API generation failed: {e}, using extractive summary")
            return self._generate_extractive_summary(prompt)
    
    def _generate_extractive_summary(self, prompt: str) -> str:
        """Fallback: Generate extractive summary using simple heuristics."""
        # Extract transcript from prompt
        transcript = prompt.split("Transcript:")[1].split("Please provide:")[0].strip()
        
        sentences = [s.strip() for s in transcript.split('.') if len(s.strip()) > 20]
        
        # Simple extractive summary - take first 10 sentences
        summary_sentences = sentences[:10]
        
        summary = f"""EXECUTIVE SUMMARY:
{'. '.join(summary_sentences[:3])}.

KEY POINTS:
• Revenue and earnings discussed
• Business performance highlighted
• Future outlook provided

Note: This is an extractive summary. For detailed analysis, use AI model."""
        
        return summary
    
    def _structure_summary(self, summary: str) -> Dict[str, Any]:
        """Parse summary into structured format."""
        sections = {
            "executive_summary": "",
            "key_metrics": [],
            "strategic_initiatives": [],
            "guidance": "",
            "tone": ""
        }
        
        # Simple parsing - split by section headers
        current_section = None
        lines = summary.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect section headers
            lower = line.lower()
            if "executive summary" in lower:
                current_section = "executive_summary"
            elif "key" in lower and ("metric" in lower or "financial" in lower):
                current_section = "key_metrics"
            elif "strategic" in lower or "initiative" in lower:
                current_section = "strategic_initiatives"
            elif "guidance" in lower or "outlook" in lower:
                current_section = "guidance"
            elif "tone" in lower:
                current_section = "tone"
            elif current_section:
                # Add content to current section
                if current_section in ["executive_summary", "guidance", "tone"]:
                    sections[current_section] += line + " "
                elif line.startswith(('•', '-', '*')) or line[0].isdigit():
                    # Bullet point
                    if current_section in ["key_metrics", "strategic_initiatives"]:
                        sections[current_section].append(line.lstrip('•-*0123456789. '))
        
        # Clean up
        sections["executive_summary"] = sections["executive_summary"].strip()
        sections["guidance"] = sections["guidance"].strip()
        sections["tone"] = sections["tone"].strip()
        
        return sections
    
    def format_output(self, raw_output: Dict[str, Any]) -> Dict[str, Any]:
        """Format output in standard structure."""
        return {
            "summary": raw_output["structured_summary"],
            "metadata": {
                "company": raw_output["company"],
                "quarter": raw_output["quarter"],
                "year": raw_output["year"],
                "transcript_length": raw_output["transcript_length"],
                "summary_length": raw_output["summary_length"],
                "compression_ratio": round(
                    raw_output["summary_length"] / raw_output["transcript_length"] * 100, 2
                )
            },
            "raw_summary": raw_output["raw_summary"]
        }
