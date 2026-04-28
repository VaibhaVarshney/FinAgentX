import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from agent.state import AgentState
from agent.analysis_engine import run_full_stock_analysis
from agent.llm_synthesizer import generate_educational_analysis

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0,  # deterministic for classification
)

# Valid intents — used for normalization after LLM response
VALID_INTENTS = {"stock_analysis", "concept_explanation", "comparison"}

# Common false positives from naive isupper() extraction
TICKER_BLACKLIST = {"I", "A", "AI", "US", "CEO", "CFO",
                    "ETF", "IPO", "Q1", "Q2", "Q3", "Q4", "GDP", "RSI", "PE"}


def _normalize_intent(raw: str) -> str:
    """
    Cleans LLM intent output and maps it to a valid category.
    Falls back to 'stock_analysis' if unrecognized.
    """
    cleaned = raw.strip().lower().replace(" ", "_").replace("-", "_")

    # Try direct match first
    if cleaned in VALID_INTENTS:
        return cleaned

    # Try partial match for robustness
    for intent in VALID_INTENTS:
        if intent in cleaned:
            return intent

    return "stock_analysis"  # safe default


def _extract_tickers(query: str) -> list[str]:
    """
    Improved ticker extraction:
    - Looks for 1-5 uppercase letter sequences
    - Filters out common English words and known false positives
    - Also handles explicit $TICKER format (e.g. $AAPL)
    """
    # Match $TICKER format first (explicit)
    dollar_tickers = re.findall(r'\$([A-Z]{1,5})', query)

    # Match plain uppercase words
    words = query.split()
    plain_tickers = [
        w.strip(".,!?") for w in words
        if re.fullmatch(r'[A-Z]{1,5}', w.strip(".,!?"))
        and w.strip(".,!?") not in TICKER_BLACKLIST
    ]

    # Dollar tickers take priority, then plain
    seen = set()
    result = []
    for t in dollar_tickers + plain_tickers:
        if t not in seen:
            seen.add(t)
            result.append(t)

    return result


def classify_intent(state: AgentState) -> AgentState:
    query = state["user_query"]

    prompt = f"""You are a financial assistant router. Classify the user's request into EXACTLY one of these categories:

- stock_analysis     → user wants analysis of a single stock
- concept_explanation → user wants to understand a financial term or concept
- comparison         → user wants to compare two or more stocks

User request: "{query}"

Reply with ONLY the category name, nothing else. No punctuation, no explanation.
"""

    raw = llm.invoke([HumanMessage(content=prompt)]).content
    intent = _normalize_intent(raw)

    return {**state, "intent": intent}


def stock_analysis_node(state: AgentState) -> AgentState:
    query = state["user_query"]

    tickers = _extract_tickers(query)
    ticker = tickers[0] if tickers else "AAPL"

    try:
        analysis = run_full_stock_analysis(ticker)
        explanation = generate_educational_analysis(analysis)
    except Exception as e:
        explanation = f"Could not complete analysis for {ticker}: {str(e)}"
        analysis = {}

    return {
        **state,
        "ticker": ticker,
        "analysis_result": analysis,
        "final_output": explanation,
    }


def concept_explanation_node(state: AgentState) -> AgentState:
    query = state["user_query"]

    prompt = f"""You are an educational finance assistant.

Explain the following financial concept clearly for beginners:

"{query}"

Structure your answer with:
1. Simple definition (1-2 sentences)
2. Why it matters in investing
3. A simple real-world example

Keep it beginner-friendly. Do not give investment advice.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return {**state, "final_output": response.content}


def comparison_node(state: AgentState) -> AgentState:
    query = state["user_query"]

    tickers = _extract_tickers(query)

    if len(tickers) < 2:
        tickers = ["AAPL", "MSFT"]

    ticker1, ticker2 = tickers[0], tickers[1]

    try:
        analysis1 = run_full_stock_analysis(ticker1)
        analysis2 = run_full_stock_analysis(ticker2)
    except Exception as e:
        return {**state, "final_output": f"Could not complete comparison: {str(e)}"}

    prompt = f"""You are an educational financial assistant.

Compare these two stocks for learning purposes. Do NOT give buy or sell advice.

{ticker1} Data:
- Price: {analysis1['current_price']} | PE: {analysis1['pe_ratio']}
- Trend: {analysis1['technical_analysis']['trend']}
- RSI: {analysis1['technical_analysis']['latest_rsi']}
- Volatility: {analysis1['risk_analysis']['annual_volatility']}
- Sharpe Ratio: {analysis1['risk_analysis']['sharpe_ratio']}
- Max Drawdown: {analysis1['risk_analysis']['max_drawdown']}

{ticker2} Data:
- Price: {analysis2['current_price']} | PE: {analysis2['pe_ratio']}
- Trend: {analysis2['technical_analysis']['trend']}
- RSI: {analysis2['technical_analysis']['latest_rsi']}
- Volatility: {analysis2['risk_analysis']['annual_volatility']}
- Sharpe Ratio: {analysis2['risk_analysis']['sharpe_ratio']}
- Max Drawdown: {analysis2['risk_analysis']['max_drawdown']}

Explain:
1. Which stock has stronger trend signals and why
2. Which stock carries higher risk and what that means
3. Key differences in technical indicators
4. Educational takeaway for a beginner learning to compare stocks
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return {**state, "final_output": response.content}
