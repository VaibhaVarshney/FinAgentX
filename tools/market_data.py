import time
import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker: str, period: str = "1y", retries: int = 3) -> dict:
    """
    Fetch historical stock data and basic info.
    Retries up to 3 times on rate limit errors.
    """

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
            raise  # Don't retry invalid tickers

        except Exception as e:
            error_msg = str(e).lower()

            if "rate limit" in error_msg or "too many requests" in error_msg:
                if attempt < retries - 1:
                    wait = 5 * (attempt + 1)  # 5s, 10s, 15s
                    time.sleep(wait)
                    continue
                else:
                    raise ValueError(
                        f"Yahoo Finance is rate limiting requests right now. "
                        f"Please wait 30 seconds and try again."
                    )
            else:
                raise ValueError(
                    f"Could not fetch data for '{ticker}': {str(e)}")

    raise ValueError(
        f"Failed to fetch data for '{ticker}' after {retries} attempts.")
