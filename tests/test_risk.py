from tools.market_data import fetch_stock_data
from tools.risk import compute_risk_metrics

data = fetch_stock_data("AAPL")

risk = compute_risk_metrics(data["historical_data"])

print("Risk Metrics:")
print(risk)
