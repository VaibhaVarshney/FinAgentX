import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from agent.state import AgentState
from agent.analysis_engine import run_full_stock_analysis
from agent.llm_synthesizer import generate_educational_analysis
from tools.ticker_resolver import resolve_tickers

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0,
)

VALID_INTENTS = {"stock_analysis", "concept_explanation", "comparison"}


def _normalize_intent(raw: str) -> str:
    cleaned = raw.strip().lower().replace(" ", "_").replace("-", "_")
    if cleaned in VALID_INTENTS:
        return cleaned
    for intent in VALID_INTENTS:
        if intent in cleaned:
            return intent
    return "stock_analysis"


def classify_intent(state: AgentState) -> AgentState:
    query = state["user_query"]
    prompt = f"""You are a financial assistant router. Classify the user's request into EXACTLY one of these categories:

- stock_analysis      → user wants analysis of a single stock or company
- concept_explanation → user wants to understand a financial term or concept
- comparison          → user wants to compare two or more stocks or companies

User request: "{query}"

Reply with ONLY the category name, nothing else.
"""
    raw = llm.invoke([HumanMessage(content=prompt)]).content
    intent = _normalize_intent(raw)
    return {**state, "intent": intent}


def stock_analysis_node(state: AgentState) -> AgentState:
    query = state["user_query"]
    tickers = resolve_tickers(query, needed=1)
    ticker = tickers[0]
    try:
        analysis = run_full_stock_analysis(ticker)
        explanation = generate_educational_analysis(analysis)
    except Exception as e:
        explanation = f"❌ Could not complete analysis for **{ticker}**: {str(e)}"
        analysis = {}
    return {**state, "ticker": ticker, "analysis_result": analysis, "final_output": explanation}


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
    tickers = resolve_tickers(query, needed=2)
    if len(tickers) < 2:
        tickers = tickers + ["MSFT"] if tickers else ["AAPL", "MSFT"]

    ticker1, ticker2 = tickers[0], tickers[1]

    try:
        analysis1 = run_full_stock_analysis(ticker1)
        analysis2 = run_full_stock_analysis(ticker2)
    except Exception as e:
        return {**state, "final_output": f"❌ Could not complete comparison: {str(e)}", "comparison_results": []}

    prompt = f"""You are an educational financial assistant.

Compare {ticker1} and {ticker2} for learning purposes. Do NOT give buy or sell advice.

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
1. Which of {ticker1} or {ticker2} has stronger trend signals and why
2. Which of {ticker1} or {ticker2} carries higher risk
3. Key differences in their technical indicators
4. Educational takeaway for a beginner comparing {ticker1} vs {ticker2}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        **state,
        "comparison_results": [analysis1, analysis2],
        "final_output": response.content,
    }
