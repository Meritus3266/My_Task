m# 🤖 Multi-Agent Earnings Call Analyzer

Production-ready multi-agent system for comprehensive analysis of earnings call transcripts using specialized AI agents.

## 🎯 What It Does

Analyzes earnings call transcripts using **3 specialized agents**:

1. **📝 Summarizer Agent** - Generates executive summaries with key metrics and insights
2. **📊 Signal Extractor Agent** - Identifies investment signals (bullish/bearish) and generates recommendations
3. **🔍 Critical Examiner Agent** - Performs deep critical analysis, identifies red flags and assesses management credibility

## ✨ Features

- **Parallel Execution** - Run all agents simultaneously for faster analysis
- **Flexible Deployment** - Use local fine-tuned models OR Claude API
- **Production Ready** - Error handling, logging, monitoring
- **Comprehensive Reports** - Structured JSON output with all findings
- **Extensible** - Easy to add new agents

## 🚀 Quick Start

### Installation

```bash
cd multi_agent_system
pip install -r requirements.txt
```

### Setup API Key (if using Claude API)

```bash
# Create .env file
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

### Run Analysis

```bash
# Analyze a transcript
python main.py path/to/MSFT_Q4_2023_earnings_transcript.txt

# Save to specific output file
python main.py transcript.txt --output my_analysis.json

# Run specific agents only
python main.py transcript.txt --agents summarizer signal_extractor

# Use local fine-tuned model
python main.py transcript.txt --model-path trained_model/final

# Run sequentially (not parallel)
python main.py transcript.txt --sequential

# Debug mode
python main.py transcript.txt --debug
```

## 📁 Project Structure

```
multi_agent_system/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py              # Base class for all agents
│   ├── summarizer_agent.py        # Summarization agent
│   ├── signal_extractor_agent.py  # Signal extraction agent
│   └── critical_examiner_agent.py # Critical analysis agent
├── orchestrator.py                # Multi-agent coordinator
├── main.py                       # Main execution script
├── requirements.txt              # Dependencies
├── outputs/                      # Analysis reports (auto-created)
└── README.md                     # This file
```

## 🤖 Agent Details

### 1. Summarizer Agent

**Purpose**: Generate concise, structured summaries

**Outputs**:
- Executive summary (2-3 sentences)
- Key financial metrics
- Strategic initiatives
- Guidance & outlook
- Management tone

**Example**:
```json
{
  "summary": {
    "executive_summary": "Microsoft reported strong Q4 results...",
    "key_metrics": [
      "Revenue up 12% YoY to $56.2B",
      "Cloud revenue grew 28%"
    ],
    "strategic_initiatives": [
      "Expanding AI integration across product suite"
    ],
    "guidance": "Expects continued double-digit growth...",
    "tone": "confident"
  }
}
```

### 2. Signal Extractor Agent

**Purpose**: Identify investment signals and generate trading recommendations

**Outputs**:
- Bullish signals (positive indicators)
- Bearish signals (warning signs)
- Risk factors
- Opportunities
- Overall signal score (-100 to +100)
- Investment recommendation (STRONG BUY/BUY/HOLD/SELL/STRONG SELL)

**Example**:
```json
{
  "signal_score": {
    "score": 45,
    "recommendation": "BUY",
    "confidence": "HIGH",
    "bullish_signals": 8,
    "bearish_signals": 2
  },
  "signals": {
    "bullish": [
      "Revenue growth accelerating",
      "Margin expansion of 200 bps"
    ],
    "bearish": [
      "FX headwinds mentioned"
    ]
  }
}
```

### 3. Critical Examiner Agent

**Purpose**: Deep critical analysis and red flag detection

**Outputs**:
- Inconsistencies & contradictions
- Red flags
- Management credibility assessment
- Question evasion detection
- Omissions (what wasn't discussed)
- Language pattern analysis

**Example**:
```json
{
  "credibility": {
    "score": 75,
    "rating": "HIGH",
    "red_flag_count": 1,
    "key_concerns": [
      "Vague guidance on margins"
    ]
  },
  "critical_analysis": {
    "red_flags": [
      "Avoided specific question about churn"
    ],
    "omissions": [
      "No mention of key competitor"
    ]
  }
}
```

## 📊 Output Format

The system generates a comprehensive JSON report:

```json
{
  "company": "MSFT",
  "quarter": "Q4",
  "year": "2023",
  "timestamp": "2024-01-15T10:30:00",
  
  "summary": { ... },
  "investment_signals": { ... },
  "critical_analysis": { ... },
  
  "overall_assessment": {
    "recommendation": "BUY",
    "confidence": "HIGH",
    "signal_score": 45,
    "credibility_score": 75,
    "risk_level": "LOW",
    "key_takeaways": [
      "Strong fundamentals with accelerating growth",
      "Management credible and transparent",
      "Few red flags identified"
    ]
  },
  
  "metadata": {
    "execution_time_seconds": 45.3,
    "agents_executed": ["summarizer", "signal_extractor", "critical_examiner"]
  }
}
```

## 🔧 Advanced Usage

### Using Local Fine-Tuned Model

If you've trained a model using the fine-tuning system:

```bash
python main.py transcript.txt --model-path trained_model/final
```

The agents will use your fine-tuned model instead of the API.

### Programmatic Usage

```python
from orchestrator import MultiAgentOrchestrator

# Initialize
orchestrator = MultiAgentOrchestrator()

# Analyze
result = orchestrator.analyze_transcript(
    transcript="Earnings call text here...",
    company="MSFT",
    quarter="Q4",
    year="2023",
    parallel=True
)

# Access results
print(result["overall_assessment"]["recommendation"])
print(result["signal_score"]["score"])

# Save report
orchestrator.save_report(result, "analysis.json")

# Get agent statistics
stats = orchestrator.get_agent_stats()
print(stats)
```

### Adding Custom Agents

Create a new agent by extending `BaseAgent`:

```python
from agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self, model=None, config=None):
        super().__init__("MyAgent", model, config)
    
    def validate_input(self, input_data):
        return isinstance(input_data, dict) and "transcript" in input_data
    
    def analyze(self, input_data):
        # Your analysis logic here
        return {"result": "my analysis"}
    
    def format_output(self, raw_output):
        return {"formatted": raw_output}
```

Then add to orchestrator:

```python
orchestrator.agents["my_agent"] = MyCustomAgent()
```

## 📈 Performance

**Typical execution times** (depends on transcript length and hardware):

- **With Claude API**: 30-60 seconds (parallel mode)
- **With Local Model**: 2-5 minutes (depends on GPU)
- **Sequential Mode**: 2-3x slower than parallel

**Resource Usage**:
- Memory: ~2GB (without local model), ~8GB (with local model)
- GPU: Optional but recommended for local model

## 🔒 Security & Privacy

- **API Keys**: Store in `.env` file, never commit
- **Transcripts**: Processed locally, not stored by agents
- **Reports**: Saved locally in `outputs/` directory
- **Logging**: Logs saved to `multi_agent_analysis.log`

## 🐛 Troubleshooting

**No output generated?**
- Check if API key is set (if using API mode)
- Verify transcript file exists and is readable
- Run with `--debug` flag to see detailed logs

**Agents failing?**
- Check API key is valid
- Ensure transcript is long enough (>100 characters)
- Try sequential mode: `--sequential`

**Local model not loading?**
- Verify model path is correct
- Ensure you have enough GPU memory
- Fall back to API mode (remove `--model-path`)

**Slow execution?**
- Use parallel mode (default)
- Consider using API instead of local model
- Reduce transcript length for testing

## 📝 Examples

### Basic Analysis
```bash
python main.py transcripts/MSFT_Q4_2023_earnings_transcript.txt
```

### Only Extract Signals
```bash
python main.py transcript.txt --agents signal_extractor
```

### Batch Processing
```bash
for file in transcripts/*.txt; do
    python main.py "$file" --output "outputs/$(basename $file .txt)_analysis.json"
done
```

### Compare Multiple Quarters
```python
from orchestrator import MultiAgentOrchestrator
import glob

orchestrator = MultiAgentOrchestrator()

for transcript_file in glob.glob("transcripts/MSFT_*.txt"):
    with open(transcript_file) as f:
        data = load_transcript(transcript_file)
    
    result = orchestrator.analyze_transcript(**data)
    
    print(f"{data['quarter']} {data['year']}: {result['overall_assessment']['recommendation']}")
```

## 🤝 Contributing

To add new agents:
1. Create new agent class extending `BaseAgent`
2. Implement required methods: `validate_input`, `analyze`, `format_output`
3. Add to `orchestrator.py`
4. Update README

## 📄 License

Free to use for personal and commercial purposes.

## 🎉 Next Steps

1. Analyze your first transcript
2. Fine-tune the agents' prompts for your use case
3. Add custom agents for specialized analysis
4. Integrate with your existing investment workflow

Happy analyzing! 📊
