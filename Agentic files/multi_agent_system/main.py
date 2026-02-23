"""
Main Script - Multi-Agent Earnings Call Analyzer
Run comprehensive analysis on earnings call transcripts.
"""

import argparse
import sys
import os
from pathlib import Path
import json
import logging

from orchestrator import MultiAgentOrchestrator


def setup_logging(debug: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('multi_agent_analysis.log')
        ]
    )


def load_transcript(filepath: str) -> dict:
    """Load transcript from file."""
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"Transcript not found: {filepath}")
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract metadata from filename if available
    # Expected format: COMPANY_QUARTER_YEAR_earnings_transcript.txt
    filename = path.stem
    parts = filename.split('_')
    
    company = parts[0] if len(parts) > 0 else "Unknown"
    quarter = parts[1] if len(parts) > 1 else "Unknown"
    year = parts[2] if len(parts) > 2 else "Unknown"
    
    # Try to extract from file content
    lines = content.split('\n')
    for line in lines[:10]:
        if line.startswith("Company"):
            company = line.split(":")[-1].strip()
        elif line.startswith("Quarter"):
            quarter = line.split(":")[-1].strip()
        elif line.startswith("Year"):
            year = line.split(":")[-1].strip()
    
    # Find where actual transcript starts (after metadata)
    transcript_start = 0
    for i, line in enumerate(lines):
        if "=" * 40 in line:
            transcript_start = i + 1
            break
    
    transcript = '\n'.join(lines[transcript_start:]).strip()
    
    return {
        "transcript": transcript,
        "company": company,
        "quarter": quarter,
        "year": year
    }


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Earnings Call Analyzer"
    )
    
    parser.add_argument(
        "transcript",
        type=str,
        help="Path to earnings call transcript file"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file for analysis report (JSON)"
    )
    
    parser.add_argument(
        "--agents",
        type=str,
        nargs="+",
        choices=["summarizer", "signal_extractor", "critical_examiner"],
        default=None,
        help="Specific agents to run (default: all)"
    )
    
    parser.add_argument(
        "--sequential",
        action="store_true",
        help="Run agents sequentially instead of parallel"
    )
    
    parser.add_argument(
        "--model-path",
        type=str,
        default=None,
        help="Path to local fine-tuned model (optional)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    try:
        # Load transcript
        logger.info(f"Loading transcript from: {args.transcript}")
        transcript_data = load_transcript(args.transcript)
        
        logger.info(f"Company: {transcript_data['company']}")
        logger.info(f"Quarter: {transcript_data['quarter']}")
        logger.info(f"Year: {transcript_data['year']}")
        logger.info(f"Transcript length: {len(transcript_data['transcript'])} characters")
        
        # Load model if specified
        model = None
        if args.model_path:
            logger.info(f"Loading model from: {args.model_path}")
            try:
                from transformers import AutoModelForCausalLM
                import torch
                
                model = AutoModelForCausalLM.from_pretrained(
                    args.model_path,
                    device_map="auto",
                    torch_dtype=torch.float16
                )
                model.eval()
                logger.info(" Model loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load model: {e}")
                logger.info("Falling back to API mode")
        
        # Initialize orchestrator
        orchestrator = MultiAgentOrchestrator(model=model)
        
        # Run analysis
        logger.info("\n" + "="*80)
        logger.info("STARTING MULTI-AGENT ANALYSIS")
        logger.info("="*80 + "\n")
        
        result = orchestrator.analyze_transcript(
            transcript=transcript_data["transcript"],
            company=transcript_data["company"],
            quarter=transcript_data["quarter"],
            year=transcript_data["year"],
            agents_to_run=args.agents,
            parallel=not args.sequential
        )
        
        # Print summary
        logger.info("\n" + "="*80)
        logger.info("ANALYSIS COMPLETE")
        logger.info("="*80)
        
        assessment = result["overall_assessment"]
        logger.info(f"\nRECOMMENDATION: {assessment['recommendation']}")
        logger.info(f"CONFIDENCE: {assessment['confidence']}")
        logger.info(f"SIGNAL SCORE: {assessment['signal_score']}")
        logger.info(f"CREDIBILITY: {assessment['credibility_rating']} ({assessment['credibility_score']}/100)")
        logger.info(f"RISK LEVEL: {assessment['risk_level']}")
        
        logger.info("\nKEY TAKEAWAYS:")
        for i, takeaway in enumerate(assessment['key_takeaways'], 1):
            logger.info(f"{i}. {takeaway}")
        
        # Save report
        if args.output:
            output_path = args.output
        else:
            output_path = f"outputs/{transcript_data['company']}_{transcript_data['quarter']}_{transcript_data['year']}_analysis.json"
        
        os.makedirs(os.path.dirname(output_path) or "outputs", exist_ok=True)
        orchestrator.save_report(result, output_path)
        
        logger.info(f"\n Full report saved to: {output_path}")
        
        # Print agent stats
        logger.info("\n" + "="*80)
        logger.info("AGENT STATISTICS")
        logger.info("="*80)
        stats = orchestrator.get_agent_stats()
        for agent_name, agent_stats in stats.items():
            logger.info(f"\n{agent_name}:")
            logger.info(f"  Executions: {agent_stats['total_executions']}")
            logger.info(f"  Success Rate: {agent_stats['success_rate']:.1f}%")
            logger.info(f"  Avg Time: {agent_stats['average_execution_time']:.2f}s")
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        return 1
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.debug:
            import traceback
            logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
