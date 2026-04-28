import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker: str, period: str = "1y"):
    """
    Fetch historical stock data and basic info.
    """

    stock = yf.Ticker(ticker)

    hist = stock.history(period=period)

    if hist.empty:
        raise ValueError(f"No data found for ticker: {ticker}")

    info = stock.info

    result = {
        "ticker": ticker.upper(),
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "historical_data": hist
    }

    return result
