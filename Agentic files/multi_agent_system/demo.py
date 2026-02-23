"""
Demo Script - Multi-Agent System
Shows how to use the multi-agent analyzer with a sample transcript.
"""

from orchestrator import MultiAgentOrchestrator
import json

# Sample earnings call transcript (shortened for demo)
SAMPLE_TRANSCRIPT = """
Microsoft Q4 FY2023 Earnings Call

Operator: Good afternoon. Welcome to Microsoft's Q4 FY2023 earnings conference call.

Satya Nadella (CEO): Thank you for joining us today. I'm pleased to report strong Q4 results.
Revenue was $56.2 billion, up 8% year-over-year. Our cloud business continues to show momentum
with Azure growing 26%. 

We're seeing incredible demand for our AI offerings. GitHub Copilot has surpassed 1 million
paid subscribers, and we're integrating AI capabilities across our entire product suite.

Our gaming business had record engagement with 120 million monthly active users on Xbox.

Looking ahead, we expect continued strong demand for cloud and AI solutions. We're investing
heavily in infrastructure to meet this demand.

Amy Hood (CFO): Thanks Satya. Our operating margins expanded by 200 basis points to 45%,
driven by operating leverage in our cloud business. 

Free cash flow was $21.5 billion, up 18% year-over-year. We returned $9.7 billion to 
shareholders through dividends and buybacks.

For Q1 FY2024, we expect revenue between $53.8 billion and $54.8 billion, representing
approximately 10% growth at the midpoint.

We're confident in our ability to deliver sustained growth while maintaining strong profitability.

Analyst Q&A:

Analyst 1: Can you provide more color on Azure growth trends?

Satya: Azure revenue grew 26%, which is strong. We're seeing particular strength in AI workloads.
Many customers are moving their AI initiatives to Azure given our partnership with OpenAI.

Analyst 2: What about pricing pressure from competitors?

Satya: We compete on value, not just price. Our integrated AI stack provides unique value.
We haven't seen significant pricing pressure.

Analyst 3: Any concerns about macro headwinds?

Amy: We're monitoring the macro environment closely. That said, digital transformation remains
a priority for our customers. We're well-positioned regardless of the economic environment.
"""

def main():
    print("=" * 80)
    print("MULTI-AGENT EARNINGS CALL ANALYZER - DEMO")
    print("=" * 80)
    print()
    
    # Initialize orchestrator
    print("Initializing multi-agent system...")
    orchestrator = MultiAgentOrchestrator()
    print("✓ Orchestrator initialized with 3 agents\n")
    
    # Run analysis
    print("Running analysis on sample Microsoft Q4 FY2023 transcript...")
    print("(This will use Claude API if ANTHROPIC_API_KEY is set, otherwise keyword analysis)\n")
    
    result = orchestrator.analyze_transcript(
        transcript=SAMPLE_TRANSCRIPT,
        company="MSFT",
        quarter="Q4",
        year="2023",
        parallel=True
    )
    
    # Display results
    print("\n" + "=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)
    
    # Overall Assessment
    assessment = result["overall_assessment"]
    print(f"\n📊 OVERALL ASSESSMENT")
    print(f"   Recommendation: {assessment['recommendation']}")
    print(f"   Confidence: {assessment['confidence']}")
    print(f"   Signal Score: {assessment['signal_score']}/100")
    print(f"   Credibility: {assessment['credibility_rating']} ({assessment['credibility_score']}/100)")
    print(f"   Risk Level: {assessment['risk_level']}")
    
    # Key Takeaways
    print(f"\n📝 KEY TAKEAWAYS:")
    for i, takeaway in enumerate(assessment.get('key_takeaways', []), 1):
        print(f"   {i}. {takeaway}")
    
    # Summary
    if result.get("summary"):
        summary = result["summary"]
        print(f"\n📄 EXECUTIVE SUMMARY:")
        if summary.get("executive_summary"):
            print(f"   {summary['executive_summary']}")
    
    # Signals
    if result.get("signal_score"):
        signals = result["signal_score"]
        print(f"\n📈 INVESTMENT SIGNALS:")
        print(f"   Bullish Signals: {signals.get('bullish_signals', 0)}")
        print(f"   Bearish Signals: {signals.get('bearish_signals', 0)}")
        print(f"   Risk Factors: {signals.get('risk_factors', 0)}")
        print(f"   Opportunities: {signals.get('opportunities', 0)}")
    
    # Critical Analysis
    if result.get("credibility_assessment"):
        cred = result["credibility_assessment"]
        print(f"\n🔍 CRITICAL ANALYSIS:")
        print(f"   Assessment: {cred.get('assessment', 'N/A')}")
        print(f"   Red Flags: {cred.get('red_flag_count', 0)}")
        print(f"   Inconsistencies: {cred.get('inconsistency_count', 0)}")
        
        concerns = cred.get('key_concerns', [])
        if concerns:
            print(f"   Top Concerns:")
            for concern in concerns:
                print(f"      • {concern}")
    
    # Execution Stats
    metadata = result.get("metadata", {})
    print(f"\n⚙️ EXECUTION INFO:")
    print(f"   Execution Time: {metadata.get('execution_time_seconds', 0):.2f} seconds")
    print(f"   Mode: {metadata.get('execution_mode', 'unknown')}")
    print(f"   Agents Used: {', '.join(metadata.get('agents_executed', []))}")
    
    # Save full report
    output_file = "demo_analysis_report.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n✓ Full analysis saved to: {output_file}")
    
    # Agent Statistics
    print(f"\n📊 AGENT STATISTICS:")
    stats = orchestrator.get_agent_stats()
    for agent_name, agent_stats in stats.items():
        print(f"\n   {agent_name.upper()}:")
        print(f"      Total Executions: {agent_stats['total_executions']}")
        print(f"      Success Rate: {agent_stats['success_rate']:.1f}%")
        print(f"      Avg Time: {agent_stats['average_execution_time']:.2f}s")
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Analyze real transcripts: python main.py path/to/transcript.txt")
    print("2. Review the full JSON report: demo_analysis_report.json")
    print("3. Customize agents for your specific needs")
    print()


if __name__ == "__main__":
    main()
