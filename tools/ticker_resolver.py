import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0,
)

# Common company name → ticker map (instant lookup, no LLM needed)
KNOWN_TICKERS = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "tesla": "TSLA",
    "nvidia": "NVDA",
    "meta": "META",
    "facebook": "META",
    "netflix": "NFLX",
    "infosys": "INFY",
    "infoysys": "INFY",  # common typo
    "tata": "TCS",
    "tcs": "TCS",
    "wipro": "WIT",
    "reliance": "RELIANCE.NS",
    "samsung": "005930.KS",
    "twitter": "X",
    "uber": "UBER",
    "airbnb": "ABNB",
    "spotify": "SPOT",
    "adobe": "ADBE",
    "intel": "INTC",
    "amd": "AMD",
    "qualcomm": "QCOM",
    "salesforce": "CRM",
    "oracle": "ORCL",
    "ibm": "IBM",
    "paypal": "PYPL",
    "shopify": "SHOP",
    "zoom": "ZM",
    "snapchat": "SNAP",
    "snap": "SNAP",
    "pinterest": "PINS",
    "lyft": "LYFT",
    "coinbase": "COIN",
    "palantir": "PLTR",
    "rivian": "RIVN",
    "lucid": "LCID",
    "ford": "F",
    "gm": "GM",
    "general motors": "GM",
    "boeing": "BA",
    "disney": "DIS",
    "walmart": "WMT",
    "target": "TGT",
    "costco": "COST",
    "nike": "NKE",
    "starbucks": "SBUX",
    "mcdonalds": "MCD",
    "coca cola": "KO",
    "pepsi": "PEP",
    "johnson": "JNJ",
    "pfizer": "PFE",
    "moderna": "MRNA",
    "jpmorgan": "JPM",
    "goldman sachs": "GS",
    "bank of america": "BAC",
    "visa": "V",
    "mastercard": "MA",
    "exxon": "XOM",
    "chevron": "CVX",
}

# Blacklist — these look like tickers but aren't
TICKER_BLACKLIST = {
    "I", "A", "AI", "US", "CEO", "CFO", "ETF", "IPO",
    "Q1", "Q2", "Q3", "Q4", "GDP", "RSI", "PE", "ME",
    "IT", "IS", "AN", "AT", "IN", "OR", "IF", "AS"
}


def _extract_explicit_tickers(query: str) -> list[str]:
    """Extract $TICKER or plain UPPERCASE tickers from query."""
    dollar_tickers = re.findall(r'\$([A-Z]{1,5})', query)
    words = query.split()
    plain_tickers = [
        w.strip(".,!?") for w in words
        if re.fullmatch(r'[A-Z]{1,5}', w.strip(".,!?"))
        and w.strip(".,!?") not in TICKER_BLACKLIST
    ]
    seen = set()
    result = []
    for t in dollar_tickers + plain_tickers:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result


def _lookup_known_names(query: str) -> list[str]:
    """Check if query contains any known company names."""
    query_lower = query.lower()
    found = []
    # Sort by length descending so "bank of america" matches before "america"
    for name, ticker in sorted(KNOWN_TICKERS.items(), key=lambda x: -len(x[0])):
        if name in query_lower and ticker not in found:
            found.append(ticker)
    return found


def _llm_extract_ticker(query: str) -> list[str]:
    """
    Use LLM as last resort to extract company name and return ticker.
    Only called when no ticker or known name found.
    """
    prompt = f"""You are a financial data assistant. Extract the stock ticker symbol(s) from the user's query.

User query: "{query}"

Rules:
- Return ONLY the ticker symbol(s), comma-separated (e.g. AAPL or AAPL,MSFT)
- Use standard US stock exchange tickers
- If you cannot identify any stock, return: UNKNOWN
- Do not return any explanation, just the ticker(s)

Ticker(s):"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)]).content.strip()
        tickers = [t.strip().upper() for t in response.split(",") if t.strip()]
        return [t for t in tickers if t != "UNKNOWN" and re.fullmatch(r'[A-Z.]{1,10}', t)]
    except Exception:
        return []


def resolve_tickers(query: str, needed: int = 1) -> list[str]:
    """
    Main resolver — tries 3 strategies in order:
    1. Explicit ticker in query ($AAPL or AAPL)
    2. Known company name lookup
    3. LLM extraction as last resort

    Returns list of ticker strings, falls back to ["AAPL"] if nothing found.
    """
    # Strategy 1: explicit tickers
    tickers = _extract_explicit_tickers(query)
    if len(tickers) >= needed:
        return tickers

    # Strategy 2: known company names
    known = _lookup_known_names(query)
    tickers = list(dict.fromkeys(tickers + known))  # merge, preserve order
    if len(tickers) >= needed:
        return tickers

    # Strategy 3: LLM extraction
    llm_tickers = _llm_extract_ticker(query)
    tickers = list(dict.fromkeys(tickers + llm_tickers))

    if tickers:
        return tickers

    # Final fallback
    return ["AAPL"]
