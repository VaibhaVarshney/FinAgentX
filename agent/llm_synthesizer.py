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
    Prepends a structured header in Python so the ticker is always correct.
    """

    ticker = stock_data['ticker']
    tech = stock_data['technical_analysis']
    risk = stock_data['risk_analysis']

    # Build a hard header in Python — not relying on LLM for this
    header = f"""📊 Stock Analysis: {ticker}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Price : ${stock_data['current_price']}
PE Ratio      : {stock_data['pe_ratio']}
Trend         : {tech['trend']}
RSI (14)      : {tech['latest_rsi']}
MA50          : {tech['ma50']}
MA200         : {tech['ma200']}
Volatility    : {risk['annual_volatility']}
Sharpe Ratio  : {risk['sharpe_ratio']}
Max Drawdown  : {risk['max_drawdown']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

    prompt = f"""You are an educational financial assistant explaining stock data to a beginner.

The stock being analyzed is {ticker}. Refer to it as "{ticker}" in every sentence.

Data:
- Trend: {tech['trend']}
- RSI: {tech['latest_rsi']}
- MA50: {tech['ma50']}, MA200: {tech['ma200']}
- Annual Volatility: {risk['annual_volatility']}
- Sharpe Ratio: {risk['sharpe_ratio']}
- Max Drawdown: {risk['max_drawdown']}

Write 4 short paragraphs for {ticker}:
1. What {ticker}'s trend tells us
2. What {ticker}'s RSI of {tech['latest_rsi']} means
3. What {ticker}'s risk metrics mean
4. One educational takeaway about {ticker}

Do NOT give buy/sell advice. Always use the name {ticker} — never say "the stock" without naming {ticker} first.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    # Prepend the hard header to the LLM response
    return header + response.content
