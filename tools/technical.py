import pandas as pd
import numpy as np


def compute_technical_indicators(historical_df: pd.DataFrame) -> dict:
    """
    Compute RSI, Moving Averages, and trend classification.
    Uses pure pandas/numpy — no pandas-ta or numba dependency.
    """

    df = historical_df.copy()

    # RSI (14-period)
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=13, adjust=False).mean()
    avg_loss = loss.ewm(com=13, adjust=False).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Moving Averages
    df["MA50"] = df["Close"].rolling(window=50).mean()
    df["MA200"] = df["Close"].rolling(window=200).mean()

    latest = df.iloc[-1]

    trend = "Sideways"
    if pd.notna(latest["MA50"]) and pd.notna(latest["MA200"]):
        if latest["MA50"] > latest["MA200"]:
            trend = "Uptrend"
        elif latest["MA50"] < latest["MA200"]:
            trend = "Downtrend"

    return {
        "latest_rsi": float(round(latest["RSI"], 2)) if pd.notna(latest["RSI"]) else None,
        "ma50": float(round(latest["MA50"], 2)) if pd.notna(latest["MA50"]) else None,
        "ma200": float(round(latest["MA200"], 2)) if pd.notna(latest["MA200"]) else None,
        "trend": trend,
    }
