import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
)


def generate_educational_analysis(stock_data: dict) -> str:
    """
    Converts structured analysis into an educational explanation using Groq LLM.
    """

    prompt = f"""
You are an educational financial assistant.

Your task is to explain stock analysis results clearly for someone learning investing.

DO NOT give buy or sell advice. Only explain what the numbers mean.

Stock data:

Ticker: {stock_data['ticker']}
Current Price: {stock_data['current_price']}
PE Ratio: {stock_data['pe_ratio']}

Technical Indicators:
RSI: {stock_data['technical_analysis']['latest_rsi']}
MA50: {stock_data['technical_analysis']['ma50']}
MA200: {stock_data['technical_analysis']['ma200']}
Trend: {stock_data['technical_analysis']['trend']}

Risk Metrics:
Annual Volatility: {stock_data['risk_analysis']['annual_volatility']}
Sharpe Ratio: {stock_data['risk_analysis']['sharpe_ratio']}
Max Drawdown: {stock_data['risk_analysis']['max_drawdown']}

Please explain:
1. What the trend indicates
2. What the RSI value means right now
3. What the risk metrics tell us
4. An educational takeaway for someone learning finance

Keep it clear, structured, and beginner-friendly.
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content
