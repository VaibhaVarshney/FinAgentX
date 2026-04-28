import pandas as pd
import pandas_ta as ta


def compute_technical_indicators(historical_df: pd.DataFrame):
    """
    Compute RSI, Moving Averages, and basic trend classification.
    """

    df = historical_df.copy()

    # RSI
    df["RSI"] = ta.rsi(df["Close"], length=14)

    # Moving Averages
    df["MA50"] = df["Close"].rolling(window=50).mean()
    df["MA200"] = df["Close"].rolling(window=200).mean()

    latest = df.iloc[-1]

    trend = "Sideways"
    if latest["MA50"] > latest["MA200"]:
        trend = "Uptrend"
    elif latest["MA50"] < latest["MA200"]:
        trend = "Downtrend"

    result = {
        "latest_rsi": float(round(latest["RSI"], 2)) if pd.notna(latest["RSI"]) else None,
        "ma50": float(round(latest["MA50"], 2)) if pd.notna(latest["MA50"]) else None,
        "ma200": float(round(latest["MA200"], 2)) if pd.notna(latest["MA200"]) else None,
        "trend": trend
    }

    return result
