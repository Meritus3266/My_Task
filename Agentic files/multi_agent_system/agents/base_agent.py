"""
Base Agent Class
Foundation for all specialized agents in the system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import json

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    
    All agents must implement:
    - analyze(): Main analysis method
    - validate_input(): Input validation
    - format_output(): Output formatting
    """
    
    def __init__(self, name: str, model=None, config: Optional[Dict] = None):
        """
        Initialize base agent.
        
        Args:
            name: Agent name
            model: LLM model instance (optional, can use API)
            config: Configuration dictionary
        """
        self.name = name
        self.model = model
        self.config = config or {}
        self.logger = self._setup_logger()
        self.execution_history = []
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for this agent."""
        logger = logging.getLogger(f"Agent.{self.name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.name} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    @abstractmethod
    def analyze(self, input_data: Any) -> Dict[str, Any]:
        """
        Main analysis method - must be implemented by subclasses.
        
        Args:
            input_data: Input to analyze
            
        Returns:
            Dictionary with analysis results
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data."""
        pass
    
    @abstractmethod
    def format_output(self, raw_output: Any) -> Dict[str, Any]:
        """Format output in standard structure."""
        pass
    
    def execute(self, input_data: Any) -> Dict[str, Any]:
        """
        Execute the agent with error handling and logging.
        
        Args:
            input_data: Input to process
            
        Returns:
            Formatted output dictionary
        """
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Starting execution")
            
            # Validate input
            if not self.validate_input(input_data):
                raise ValueError(f"Invalid input for {self.name}")
            
            # Perform analysis
            raw_result = self.analyze(input_data)
            
            # Format output
            formatted_result = self.format_output(raw_result)
            
            # Add metadata
            execution_time = (datetime.now() - start_time).total_seconds()
            result = {
                "agent": self.name,
                "timestamp": datetime.now().isoformat(),
                "execution_time_seconds": execution_time,
                "status": "success",
                **formatted_result
            }
            
            # Log execution
            self._log_execution(result)
            
            self.logger.info(f"Completed in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Execution failed: {e}")
            
            error_result = {
                "agent": self.name,
                "timestamp": datetime.now().isoformat(),
                "execution_time_seconds": execution_time,
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__
            }
            
            self._log_execution(error_result)
            return error_result
    
    def _log_execution(self, result: Dict[str, Any]):
        """Log execution to history."""
        self.execution_history.append(result)
        
        # Keep only last 100 executions
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent execution statistics."""
        if not self.execution_history:
            return {
                "agent": self.name,
                "total_executions": 0,
                "success_rate": 0.0,
                "average_time": 0.0
            }
        
        total = len(self.execution_history)
        successes = sum(1 for r in self.execution_history if r["status"] == "success")
        avg_time = sum(r["execution_time_seconds"] for r in self.execution_history) / total
        
        return {
            "agent": self.name,
            "total_executions": total,
            "successful": successes,
            "failed": total - successes,
            "success_rate": (successes / total) * 100,
            "average_execution_time": avg_time,
            "last_execution": self.execution_history[-1]["timestamp"]
        }
