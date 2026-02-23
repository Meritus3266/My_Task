"""
Multi-Agent Orchestrator
Coordinates multiple agents to analyze earnings call transcripts.
"""

from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from datetime import datetime
import json

from agents.summarizer_agent import SummarizerAgent
from agents.signal_extractor_agent import SignalExtractorAgent
from agents.critical_examiner_agent import CriticalExaminerAgent


class MultiAgentOrchestrator:
    """
    Orchestrates multiple agents for comprehensive earnings call analysis.
    
    Features:
    - Parallel execution of agents
    - Result aggregation
    - Error handling
    - Performance monitoring
    """
    
    def __init__(self, model=None, config: Optional[Dict] = None):
        """
        Initialize orchestrator with agents.
        
        Args:
            model: Optional LLM model (otherwise uses API)
            config: Configuration dictionary
        """
        self.config = config or {}
        self.model = model
        
        # Initialize agents
        self.summarizer = SummarizerAgent(model, config)
        self.signal_extractor = SignalExtractorAgent(model, config)
        self.critical_examiner = CriticalExaminerAgent(model, config)
        
        self.agents = {
            "summarizer": self.summarizer,
            "signal_extractor": self.signal_extractor,
            "critical_examiner": self.critical_examiner
        }
        
        # Setup logging
        self.logger = logging.getLogger("Orchestrator")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - Orchestrator - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        self.execution_history = []
    
    def analyze_transcript(
        self,
        transcript: str,
        company: str = "Unknown",
        quarter: str = "Unknown",
        year: str = "Unknown",
        agents_to_run: Optional[List[str]] = None,
        parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze transcript using multiple agents.
        
        Args:
            transcript: Earnings call transcript text
            company: Company name
            quarter: Quarter (Q1, Q2, Q3, Q4)
            year: Year
            agents_to_run: List of agent names to run (default: all)
            parallel: Run agents in parallel (default: True)
            
        Returns:
            Comprehensive analysis results
        """
        start_time = datetime.now()
        
        self.logger.info("="*80)
        self.logger.info(f"Starting analysis: {company} {quarter} {year}")
        self.logger.info("="*80)
        
        # Prepare input data
        input_data = {
            "transcript": transcript,
            "company": company,
            "quarter": quarter,
            "year": year
        }
        
        # Determine which agents to run
        if agents_to_run is None:
            agents_to_run = list(self.agents.keys())
        
        # Validate agent names
        invalid_agents = [a for a in agents_to_run if a not in self.agents]
        if invalid_agents:
            raise ValueError(f"Invalid agents: {invalid_agents}")
        
        # Execute agents
        if parallel:
            results = self._execute_parallel(input_data, agents_to_run)
        else:
            results = self._execute_sequential(input_data, agents_to_run)
        
        # Aggregate results
        aggregated = self._aggregate_results(results, input_data)
        
        # Add metadata
        execution_time = (datetime.now() - start_time).total_seconds()
        aggregated["metadata"]["execution_time_seconds"] = execution_time
        aggregated["metadata"]["execution_mode"] = "parallel" if parallel else "sequential"
        aggregated["metadata"]["agents_executed"] = agents_to_run
        
        # Log execution
        self._log_execution(aggregated)
        
        self.logger.info(f"Analysis completed in {execution_time:.2f}s")
        
        return aggregated
    
    def _execute_parallel(
        self,
        input_data: Dict[str, Any],
        agent_names: List[str]
    ) -> Dict[str, Any]:
        """Execute agents in parallel using ThreadPoolExecutor."""
        self.logger.info(f"Executing {len(agent_names)} agents in parallel")
        
        results = {}
        
        with ThreadPoolExecutor(max_workers=len(agent_names)) as executor:
            # Submit all agent tasks
            future_to_agent = {
                executor.submit(self.agents[name].execute, input_data): name
                for name in agent_names
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_agent):
                agent_name = future_to_agent[future]
                try:
                    result = future.result()
                    results[agent_name] = result
                    self.logger.info(f"✓ {agent_name} completed")
                except Exception as e:
                    self.logger.error(f"✗ {agent_name} failed: {e}")
                    results[agent_name] = {
                        "agent": agent_name,
                        "status": "error",
                        "error": str(e)
                    }
        
        return results
    
    def _execute_sequential(
        self,
        input_data: Dict[str, Any],
        agent_names: List[str]
    ) -> Dict[str, Any]:
        """Execute agents sequentially."""
        self.logger.info(f"Executing {len(agent_names)} agents sequentially")
        
        results = {}
        
        for agent_name in agent_names:
            try:
                self.logger.info(f"Running {agent_name}...")
                result = self.agents[agent_name].execute(input_data)
                results[agent_name] = result
                self.logger.info(f"✓ {agent_name} completed")
            except Exception as e:
                self.logger.error(f"✗ {agent_name} failed: {e}")
                results[agent_name] = {
                    "agent": agent_name,
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def _aggregate_results(
        self,
        agent_results: Dict[str, Any],
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Aggregate results from all agents into comprehensive report."""
        
        # Extract successful results
        summary = agent_results.get("summarizer", {})
        signals = agent_results.get("signal_extractor", {})
        critical = agent_results.get("critical_examiner", {})
        
        # Build comprehensive report
        report = {
            "company": input_data["company"],
            "quarter": input_data["quarter"],
            "year": input_data["year"],
            "timestamp": datetime.now().isoformat(),
            
            # Summary section
            "summary": summary.get("summary", {}),
            
            # Signals section
            "investment_signals": signals.get("signals", {}),
            "signal_score": signals.get("signal_score", {}),
            
            # Critical analysis section
            "critical_analysis": critical.get("critical_analysis", {}),
            "credibility_assessment": critical.get("credibility", {}),
            
            # Overall assessment
            "overall_assessment": self._generate_overall_assessment(
                summary, signals, critical
            ),
            
            # Metadata
            "metadata": {
                "company": input_data["company"],
                "quarter": input_data["quarter"],
                "year": input_data["year"],
                "transcript_length": len(input_data["transcript"]),
                "analysis_timestamp": datetime.now().isoformat()
            },
            
            # Individual agent results (for debugging)
            "agent_results": agent_results
        }
        
        return report
    
    def _generate_overall_assessment(
        self,
        summary: Dict,
        signals: Dict,
        critical: Dict
    ) -> Dict[str, Any]:
        """Generate overall investment assessment."""
        
        # Extract key metrics
        signal_score = signals.get("signal_score", {}).get("score", 0)
        recommendation = signals.get("signal_score", {}).get("recommendation", "HOLD")
        credibility_score = critical.get("credibility", {}).get("score", 50)
        credibility_rating = critical.get("credibility", {}).get("rating", "MEDIUM")
        
        # Adjust recommendation based on credibility
        if credibility_score < 40:
            if recommendation in ["STRONG BUY", "BUY"]:
                recommendation = "HOLD"  # Downgrade due to credibility concerns
        
        # Calculate confidence
        if credibility_score >= 70 and abs(signal_score) > 30:
            confidence = "HIGH"
        elif credibility_score >= 50 and abs(signal_score) > 10:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        
        # Generate key takeaways
        takeaways = []
        
        # From summary
        exec_summary = summary.get("summary", {}).get("executive_summary", "")
        if exec_summary:
            takeaways.append(f"Summary: {exec_summary[:200]}...")
        
        # From signals
        if signal_score > 30:
            takeaways.append(f"Strong bullish signals detected (score: {signal_score})")
        elif signal_score < -30:
            takeaways.append(f"Strong bearish signals detected (score: {signal_score})")
        
        # From critical analysis
        red_flags = critical.get("credibility", {}).get("red_flag_count", 0)
        if red_flags > 2:
            takeaways.append(f"⚠️ {red_flags} red flags identified - exercise caution")
        
        return {
            "recommendation": recommendation,
            "confidence": confidence,
            "signal_score": signal_score,
            "credibility_score": credibility_score,
            "credibility_rating": credibility_rating,
            "key_takeaways": takeaways,
            "risk_level": "HIGH" if credibility_score < 40 or red_flags > 3 else "MEDIUM" if credibility_score < 70 else "LOW"
        }
    
    def _log_execution(self, result: Dict[str, Any]):
        """Log execution to history."""
        self.execution_history.append({
            "timestamp": result["timestamp"],
            "company": result["company"],
            "quarter": result["quarter"],
            "year": result["year"],
            "execution_time": result["metadata"].get("execution_time_seconds", 0),
            "recommendation": result["overall_assessment"]["recommendation"]
        })
        
        # Keep only last 100
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
    
    def get_agent_stats(self) -> Dict[str, Any]:
        """Get statistics for all agents."""
        return {
            agent_name: agent.get_stats()
            for agent_name, agent in self.agents.items()
        }
    
    def save_report(self, report: Dict[str, Any], filepath: str):
        """Save analysis report to file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Report saved to: {filepath}")
