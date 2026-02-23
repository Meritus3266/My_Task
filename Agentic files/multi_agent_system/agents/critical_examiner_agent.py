"""
Critical Examiner Agent
Performs deep critical analysis of earnings call transcripts.
"""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent


class CriticalExaminerAgent(BaseAgent):
    """
    Critically examines earnings calls for:
    - Inconsistencies
    - Red flags
    - Management credibility
    - Question evasion
    - Omissions
    - Competitive positioning
    """
    
    def __init__(self, model=None, config=None):
        super().__init__("CriticalExaminer", model, config)
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input."""
        if not input_data:
            return False
        
        if isinstance(input_data, dict):
            return "transcript" in input_data
        
        return isinstance(input_data, str) and len(input_data) > 100
    
    def analyze(self, input_data: Any) -> Dict[str, Any]:
        """Perform critical examination of transcript."""
        
        # Extract transcript
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
        
        self.logger.info(f"Critically examining {len(transcript)} characters")
        
        # Create critical analysis prompt
        prompt = f"""As a critical analyst, examine this earnings call transcript for RED FLAGS and CONCERNS.

Transcript:
{transcript[:4000]}

Perform CRITICAL ANALYSIS on:

1. INCONSISTENCIES & CONTRADICTIONS:
   - Conflicting statements about performance
   - Numbers that don't add up
   - Discrepancies with prior guidance
   - Contradictions between prepared remarks and Q&A

2. RED FLAGS:
   - Vague or evasive answers
   - Excessive use of non-GAAP metrics
   - Unexplained changes in accounting
   - One-time charges that keep recurring
   - Downplaying of issues
   - Deflecting tough questions

3. MANAGEMENT CREDIBILITY:
   - Track record of meeting guidance
   - Transparency in communication
   - Acknowledging problems vs. over-optimism
   - Quality of answers to analyst questions

4. WHAT'S NOT BEING SAID:
   - Key metrics not mentioned
   - Competitors not addressed
   - Industry trends ignored
   - Customer concerns avoided

5. COMPETITIVE POSITIONING:
   - How does this compare to competitors?
   - Market share trends
   - Pricing power indicators
   - Differentiation claims

6. QUESTION EVASION:
   - Which analyst questions were dodged?
   - Topics management avoided
   - Non-answers disguised as answers

7. LANGUAGE ANALYSIS:
   - Hedge words ("maybe", "hopefully", "trying")
   - Defensive language
   - Overly technical jargon to obscure
   - Tone shifts during difficult questions

Rate overall CREDIBILITY: High / Medium / Low
List TOP 3 CONCERNS

Be SKEPTICAL. Look for what management is trying to hide."""
        
        # Generate critical analysis
        if self.model:
            raw_analysis = self._generate_with_model(prompt)
        else:
            raw_analysis = self._generate_with_api(prompt)
        
        # Structure the analysis
        structured_analysis = self._structure_analysis(raw_analysis, transcript)
        
        # Calculate credibility score
        credibility = self._assess_credibility(structured_analysis)
        
        return {
            "company": company,
            "quarter": quarter,
            "year": year,
            "critical_analysis": structured_analysis,
            "credibility_assessment": credibility,
            "raw_analysis": raw_analysis
        }
    
    def _generate_with_model(self, prompt: str) -> str:
        """Generate analysis using local model."""
        try:
            from transformers import AutoTokenizer
            import torch
            
            tokenizer = AutoTokenizer.from_pretrained("trained_model/final")
            inputs = tokenizer(prompt, return_tensors="pt", max_length=2048, truncation=True)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs.to(self.model.device),
                    max_new_tokens=1000,
                    temperature=0.6,
                    do_sample=True
                )
            
            analysis = tokenizer.decode(outputs[0], skip_special_tokens=True)
            analysis = analysis[len(prompt):].strip()
            return analysis
            
        except Exception as e:
            self.logger.error(f"Model generation failed: {e}")
            return self._analyze_with_heuristics(prompt)
    
    def _generate_with_api(self, prompt: str) -> str:
        """Generate analysis using Claude API."""
        try:
            import anthropic
            import os
            
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
            
        except Exception as e:
            self.logger.warning(f"API failed: {e}, using heuristic analysis")
            return self._analyze_with_heuristics(prompt)
    
    def _analyze_with_heuristics(self, prompt: str) -> str:
        """Fallback: Analyze using pattern matching."""
        transcript = prompt.split("Transcript:")[1].split("Perform CRITICAL")[0].strip()
        transcript_lower = transcript.lower()
        
        # Red flag patterns
        hedge_words = ["maybe", "hopefully", "trying", "attempting", "challenging"]
        evasive_phrases = ["as i said", "like i mentioned", "we'll get back", "can't comment"]
        red_flags = []
        
        # Count hedge words
        hedge_count = sum(transcript_lower.count(word) for word in hedge_words)
        if hedge_count > 10:
            red_flags.append(f"Excessive hedging language ({hedge_count} instances)")
        
        # Look for evasive language
        evasive_count = sum(transcript_lower.count(phrase) for phrase in evasive_phrases)
        if evasive_count > 3:
            red_flags.append(f"Evasive responses detected ({evasive_count} instances)")
        
        # Check for negative terms
        negative_terms = ["decline", "weak", "challenge", "headwind", "pressure", "difficult"]
        negative_count = sum(transcript_lower.count(term) for term in negative_terms)
        
        # Check for positive spin
        positive_spin = ["despite", "however", "that said", "on the other hand"]
        spin_count = sum(transcript_lower.count(phrase) for phrase in positive_spin)
        
        analysis = f"""CRITICAL ANALYSIS (Pattern-Based):

RED FLAGS DETECTED:
{chr(10).join(f'• {flag}' for flag in red_flags) if red_flags else '• No major red flags detected'}

LANGUAGE PATTERNS:
• Hedge words: {hedge_count} instances
• Evasive phrases: {evasive_count} instances
• Negative terms: {negative_count} mentions
• Positive spin attempts: {spin_count} instances

CONCERNS:
1. {"High use of hedging language suggests uncertainty" if hedge_count > 10 else "Language appears relatively confident"}
2. {"Management appears evasive on certain topics" if evasive_count > 3 else "Management responses seem direct"}
3. {"Significant challenges acknowledged" if negative_count > 15 else "Relatively positive discussion"}

CREDIBILITY RATING: {'Low' if len(red_flags) > 2 else 'Medium' if len(red_flags) > 0 else 'High'}

Note: This is a pattern-based analysis. For deeper insights, use AI model."""
        
        return analysis
    
    def _structure_analysis(self, raw_analysis: str, transcript: str) -> Dict[str, Any]:
        """Structure the critical analysis."""
        analysis = {
            "inconsistencies": [],
            "red_flags": [],
            "credibility_issues": [],
            "omissions": [],
            "question_evasion": [],
            "language_concerns": [],
            "competitive_concerns": [],
            "top_concerns": []
        }
        
        lines = raw_analysis.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            lower = line.lower()
            
            # Detect sections
            if "inconsisten" in lower or "contradict" in lower:
                current_section = "inconsistencies"
            elif "red flag" in lower:
                current_section = "red_flags"
            elif "credibility" in lower and "concern" not in lower:
                current_section = "credibility_issues"
            elif "not being said" in lower or "omission" in lower:
                current_section = "omissions"
            elif "evasion" in lower or "avoided" in lower or "dodged" in lower:
                current_section = "question_evasion"
            elif "language" in lower:
                current_section = "language_concerns"
            elif "competitive" in lower or "competitor" in lower:
                current_section = "competitive_concerns"
            elif "top" in lower and "concern" in lower:
                current_section = "top_concerns"
            elif line.startswith(('•', '-', '*', '1', '2', '3')):
                # Bullet point or numbered item
                item = line.lstrip('•-*0123456789. ').strip()
                if current_section and item:
                    analysis[current_section].append(item)
        
        return analysis
    
    def _assess_credibility(self, analysis: Dict) -> Dict[str, Any]:
        """Assess overall management credibility."""
        
        # Count concerns
        total_red_flags = len(analysis.get("red_flags", []))
        total_inconsistencies = len(analysis.get("inconsistencies", []))
        total_evasions = len(analysis.get("question_evasion", []))
        
        # Calculate score (0-100, higher is better)
        deductions = (total_red_flags * 15) + (total_inconsistencies * 20) + (total_evasions * 10)
        score = max(0, 100 - deductions)
        
        # Determine rating
        if score >= 80:
            rating = "HIGH"
            assessment = "Management appears credible and transparent"
        elif score >= 60:
            rating = "MEDIUM"
            assessment = "Some concerns but generally acceptable"
        elif score >= 40:
            rating = "LOW"
            assessment = "Significant credibility concerns"
        else:
            rating = "VERY LOW"
            assessment = "Major red flags - exercise extreme caution"
        
        return {
            "score": score,
            "rating": rating,
            "assessment": assessment,
            "red_flag_count": total_red_flags,
            "inconsistency_count": total_inconsistencies,
            "evasion_count": total_evasions,
            "key_concerns": analysis.get("top_concerns", [])[:3]
        }
    
    def format_output(self, raw_output: Dict[str, Any]) -> Dict[str, Any]:
        """Format output in standard structure."""
        return {
            "critical_analysis": raw_output["critical_analysis"],
            "credibility": raw_output["credibility_assessment"],
            "metadata": {
                "company": raw_output["company"],
                "quarter": raw_output["quarter"],
                "year": raw_output["year"]
            },
            "raw_analysis": raw_output["raw_analysis"]
        }
