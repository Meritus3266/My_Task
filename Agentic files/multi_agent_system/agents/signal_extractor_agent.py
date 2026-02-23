"""
Signal Extraction Agent
Identifies investment signals and trading opportunities from earnings transcripts.
"""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent
import re


class SignalExtractorAgent(BaseAgent):
    """
    Extracts actionable investment signals from earnings calls.
    
    Identifies:
    - Bullish signals (positive indicators)
    - Bearish signals (negative indicators)
    - Risk factors
    - Opportunities
    - Sentiment shifts
    """
    
    def __init__(self, model=None, config=None):
        super().__init__("SignalExtractor", model, config)
        self.signal_types = ["bullish", "bearish", "neutral", "mixed"]
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input."""
        if not input_data:
            return False
        
        if isinstance(input_data, dict):
            return "transcript" in input_data
        
        return isinstance(input_data, str) and len(input_data) > 100
    
    def analyze(self, input_data: Any) -> Dict[str, Any]:
        """Extract investment signals from transcript."""
        
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
        
        self.logger.info(f"Extracting signals from {len(transcript)} characters")
        
        # Create prompt for signal extraction
        prompt = f"""Analyze this earnings call transcript and extract ACTIONABLE INVESTMENT SIGNALS.

Transcript:
{transcript[:4000]}

Identify:

1. BULLISH SIGNALS (positive indicators):
   - Revenue growth acceleration
   - Margin expansion
   - Market share gains
   - New product success
   - Positive guidance
   - Strong demand indicators

2. BEARISH SIGNALS (warning signs):
   - Revenue slowdown
   - Margin compression
   - Competitive pressure
   - Execution issues
   - Lowered guidance
   - Weakening demand

3. KEY RISK FACTORS:
   - Macro headwinds
   - Regulatory concerns
   - Operational challenges

4. OPPORTUNITIES:
   - New markets
   - Strategic initiatives
   - Cost optimization

5. SENTIMENT ANALYSIS:
   - Management confidence level
   - Tone shifts from previous quarters
   - Forward-looking language

For each signal, provide:
- Type (bullish/bearish)
- Strength (high/medium/low)
- Supporting evidence from transcript
- Potential impact

Format as structured sections."""
        
        # Generate signals
        if self.model:
            raw_signals = self._generate_with_model(prompt)
        else:
            raw_signals = self._generate_with_api(prompt)
        
        # Structure the signals
        structured_signals = self._structure_signals(raw_signals, transcript)
        
        # Calculate overall signal score
        signal_score = self._calculate_signal_score(structured_signals)
        
        return {
            "company": company,
            "quarter": quarter,
            "year": year,
            "signals": structured_signals,
            "signal_score": signal_score,
            "raw_analysis": raw_signals
        }
    
    def _generate_with_model(self, prompt: str) -> str:
        """Generate signals using local model."""
        try:
            from transformers import AutoTokenizer
            import torch
            
            tokenizer = AutoTokenizer.from_pretrained("trained_model/final")
            inputs = tokenizer(prompt, return_tensors="pt", max_length=2048, truncation=True)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs.to(self.model.device),
                    max_new_tokens=800,
                    temperature=0.5,  # Lower temperature for more focused analysis
                    do_sample=True
                )
            
            analysis = tokenizer.decode(outputs[0], skip_special_tokens=True)
            analysis = analysis[len(prompt):].strip()
            return analysis
            
        except Exception as e:
            self.logger.error(f"Model generation failed: {e}")
            return self._extract_keyword_signals(prompt)
    
    def _generate_with_api(self, prompt: str) -> str:
        """Generate signals using Claude API."""
        try:
            import anthropic
            import os
            
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
            
        except Exception as e:
            self.logger.warning(f"API failed: {e}, using keyword extraction")
            return self._extract_keyword_signals(prompt)
    
    def _extract_keyword_signals(self, prompt: str) -> str:
        """Fallback: Extract signals using keyword matching."""
        transcript = prompt.split("Transcript:")[1].split("Identify:")[0].strip()
        transcript_lower = transcript.lower()
        
        # Keyword patterns
        bullish_keywords = [
            "strong growth", "exceeded expectations", "record revenue",
            "margin expansion", "market share", "positive outlook",
            "accelerating", "outperform", "robust demand"
        ]
        
        bearish_keywords = [
            "headwind", "challenge", "pressure", "decline",
            "weak", "disappointing", "below expectations",
            "slowdown", "concern", "cautious"
        ]
        
        bullish_found = [kw for kw in bullish_keywords if kw in transcript_lower]
        bearish_found = [kw for kw in bearish_keywords if kw in transcript_lower]
        
        analysis = f"""SIGNAL EXTRACTION (Keyword-Based):

BULLISH SIGNALS DETECTED ({len(bullish_found)}):
{chr(10).join(f'• {kw.title()}' for kw in bullish_found[:5])}

BEARISH SIGNALS DETECTED ({len(bearish_found)}):
{chr(10).join(f'• {kw.title()}' for kw in bearish_found[:5])}

OVERALL SIGNAL: {'Bullish' if len(bullish_found) > len(bearish_found) else 'Bearish' if len(bearish_found) > len(bullish_found) else 'Mixed'}

Note: This is a keyword-based analysis. For deeper insights, use AI model."""
        
        return analysis
    
    def _structure_signals(self, raw_signals: str, transcript: str) -> Dict[str, List[Dict]]:
        """Parse signals into structured format."""
        signals = {
            "bullish": [],
            "bearish": [],
            "risks": [],
            "opportunities": [],
            "sentiment": {}
        }
        
        # Parse sections
        lines = raw_signals.split('\n')
        current_category = None
        current_signal = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            lower = line.lower()
            
            # Detect category headers
            if "bullish" in lower and "signal" in lower:
                current_category = "bullish"
            elif "bearish" in lower and "signal" in lower:
                current_category = "bearish"
            elif "risk" in lower:
                current_category = "risks"
            elif "opportunit" in lower:
                current_category = "opportunities"
            elif "sentiment" in lower:
                current_category = "sentiment"
            elif line.startswith(('•', '-', '*')) or (len(line) > 0 and line[0].isdigit()):
                # This is a signal item
                signal_text = line.lstrip('•-*0123456789. ').strip()
                
                if current_category in ["bullish", "bearish", "risks", "opportunities"]:
                    # Extract strength if mentioned
                    strength = "medium"
                    if "high" in signal_text.lower():
                        strength = "high"
                    elif "low" in signal_text.lower():
                        strength = "low"
                    
                    signals[current_category].append({
                        "description": signal_text,
                        "strength": strength,
                        "category": current_category
                    })
        
        # Extract sentiment
        sentiment_text = raw_signals.lower()
        if "confident" in sentiment_text or "optimistic" in sentiment_text:
            signals["sentiment"]["tone"] = "positive"
            signals["sentiment"]["confidence"] = "high"
        elif "cautious" in sentiment_text or "concern" in sentiment_text:
            signals["sentiment"]["tone"] = "cautious"
            signals["sentiment"]["confidence"] = "medium"
        else:
            signals["sentiment"]["tone"] = "neutral"
            signals["sentiment"]["confidence"] = "medium"
        
        return signals
    
    def _calculate_signal_score(self, signals: Dict) -> Dict[str, Any]:
        """Calculate overall signal score."""
        bullish_count = len(signals.get("bullish", []))
        bearish_count = len(signals.get("bearish", []))
        risk_count = len(signals.get("risks", []))
        opportunity_count = len(signals.get("opportunities", []))
        
        # Calculate weighted score (-100 to +100)
        score = (bullish_count * 10) - (bearish_count * 10) + (opportunity_count * 5) - (risk_count * 5)
        score = max(-100, min(100, score))  # Clamp to range
        
        # Determine recommendation
        if score > 30:
            recommendation = "STRONG BUY"
        elif score > 10:
            recommendation = "BUY"
        elif score > -10:
            recommendation = "HOLD"
        elif score > -30:
            recommendation = "SELL"
        else:
            recommendation = "STRONG SELL"
        
        return {
            "score": score,
            "recommendation": recommendation,
            "bullish_signals": bullish_count,
            "bearish_signals": bearish_count,
            "risk_factors": risk_count,
            "opportunities": opportunity_count,
            "confidence": signals.get("sentiment", {}).get("confidence", "medium")
        }
    
    def format_output(self, raw_output: Dict[str, Any]) -> Dict[str, Any]:
        """Format output in standard structure."""
        return {
            "signals": raw_output["signals"],
            "signal_score": raw_output["signal_score"],
            "metadata": {
                "company": raw_output["company"],
                "quarter": raw_output["quarter"],
                "year": raw_output["year"]
            },
            "raw_analysis": raw_output["raw_analysis"]
        }
