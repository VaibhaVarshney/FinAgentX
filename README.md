# FinAgentX 🤖📈

A local, free, AI-powered financial education agent built with **Groq (llama3-8b-8192)**, **LangChain**, and **LangGraph**.

> ⚠️ **Disclaimer:** FinAgentX is for **educational purposes only**. It does not provide financial advice. Do not make investment decisions based on its output.

---

## Features

- 📊 **Stock Analysis** — Fetches real-time data and computes RSI, Moving Averages, trend, volatility, Sharpe Ratio, and Max Drawdown
- 📚 **Concept Explanation** — Explains financial terms (RSI, Sharpe Ratio, PE Ratio, etc.) in plain English
- ⚖️ **Stock Comparison** — Compares two stocks side-by-side on technical and risk metrics
- ⚡ **Powered by Groq** — Fast, free LLM inference (no local GPU needed)

---

## Project Structure

```
FinAgentX/
├── agent/
│   ├── state.py              # LangGraph state definition
│   ├── nodes.py              # Intent classifier + analysis nodes
│   ├── graph.py              # LangGraph routing graph
│   ├── analysis_engine.py    # Orchestrates market + technical + risk tools
│   └── llm_synthesizer.py    # Generates educational explanations via Groq
│
├── tools/
│   ├── market_data.py        # Fetches stock data via yfinance
│   ├── technical.py          # RSI, MA50, MA200, trend
│   └── risk.py               # Volatility, Sharpe Ratio, Max Drawdown
│
├── tests/
│   ├── test_agent.py         # Full agent pipeline test
│   ├── test_llm.py           # Groq connection test
│   ├── test_market.py        # Market data fetch test
│   ├── test_technical.py     # Technical indicators test
│   ├── test_risk.py          # Risk metrics test
│   ├── test_full_analysis.py # Full analysis pipeline test
│   └── test_llm_analysis.py  # LLM explanation test
│
├── main.py                   # CLI entry point
├── requirements.txt
├── .env.example              # API key template
├── .gitignore
└── README.md
```

---

## Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/your-username/FinAgentX.git
cd FinAgentX
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your Groq API key

- Get a free key at [console.groq.com](https://console.groq.com) (no credit card required)
- Copy the example env file and add your key:

```bash
cp .env.example .env
```

Edit `.env`:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### 5. Run the agent

```bash
python main.py
```

---

## Example Queries

```
You: Analyze AAPL
You: Compare TSLA and NVDA
You: What is the Sharpe Ratio?
You: Explain RSI in simple terms
You: Analyze $MSFT
```

---

## Architecture

```
User Query
    ↓
Intent Classifier (Groq)
    ↓
LangGraph Router
    ↓
┌─────────────────────────────────────┐
│  stock_analysis  │  concept_explain  │  comparison  │
└─────────────────────────────────────┘
    ↓
Tool Execution (yfinance + pandas)
    ↓
LLM Educational Explanation (Groq)
```

---

## Tech Stack

| Component | Tool |
|---|---|
| LLM | Groq — `llama3-8b-8192` (free) |
| Agent Framework | LangGraph + LangChain |
| Market Data | yfinance |
| Technical Analysis | pandas-ta |
| Risk Metrics | numpy + pandas |
| Environment | python-dotenv |

---

## Running Tests

```bash
# Test Groq connection
python tests/test_llm.py

# Test market data fetch
python tests/test_market.py

# Test full agent pipeline
python tests/test_agent.py
```

---

## License

MIT License — free to use and modify.
