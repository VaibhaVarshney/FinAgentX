import time
import yfinance as yf
import pandas as pd
import streamlit as st


@st.cache_data(ttl=600)  # cache for 10 minutes
def fetch_stock_data(ticker: str, period: str = "1y") -> dict:
    """
    Fetch historical stock data and basic info.
    Cached for 10 minutes to avoid rate limiting.
    Retries up to 3 times on rate limit errors.
    """
    retries = 3
    for attempt in range(retries):
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)

            if hist.empty:
                raise ValueError(
                    f"No data found for ticker: {ticker}. Please check the ticker symbol.")

            info = stock.info

            return {
                "ticker": ticker.upper(),
                "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "historical_data": hist,
            }

        except ValueError:
            raise

        except Exception as e:
            error_msg = str(e).lower()
            if "rate limit" in error_msg or "too many requests" in error_msg or "429" in error_msg:
                if attempt < retries - 1:
                    time.sleep(8 * (attempt + 1))
                    continue
                else:
                    raise ValueError(
                        "Yahoo Finance is rate limiting requests. Please wait 30 seconds and try again.")
            else:
                raise ValueError(
                    f"Could not fetch data for '{ticker}': {str(e)}")
