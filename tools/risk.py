import numpy as np
import pandas as pd


def compute_risk_metrics(historical_df: pd.DataFrame) -> dict:
    """
    Compute volatility, Sharpe ratio, and max drawdown.
    """

    df = historical_df.copy()
    returns = df["Close"].pct_change().dropna()

    if len(returns) == 0:
        raise ValueError("Not enough data to compute risk metrics.")

    # Annualized Volatility
    volatility = np.std(returns) * np.sqrt(252)

    # Sharpe Ratio (risk-free rate assumed 0 for simplicity)
    sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252)

    # Maximum Drawdown
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()

    return {
        "annual_volatility": float(round(volatility, 4)),
        "sharpe_ratio": float(round(sharpe_ratio, 4)),
        "max_drawdown": float(round(max_drawdown, 4)),
    }
