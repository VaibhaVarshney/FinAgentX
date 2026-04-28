from tools.market_data import fetch_stock_data
from tools.technical import compute_technical_indicators
from tools.risk import compute_risk_metrics


def run_full_stock_analysis(ticker: str) -> dict:
    """
    Runs full pipeline: market data → technical indicators → risk metrics.
    Raises ValueError if ticker is invalid or data is unavailable.
    """

    market_data = fetch_stock_data(ticker)

    technical = compute_technical_indicators(market_data["historical_data"])
    risk = compute_risk_metrics(market_data["historical_data"])

    return {
        "ticker": market_data["ticker"],
        "current_price": market_data["current_price"],
        "market_cap": market_data["market_cap"],
        "pe_ratio": market_data["pe_ratio"],
        "technical_analysis": technical,
        "risk_analysis": risk,
    }
