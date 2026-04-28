from tools.market_data import fetch_stock_data
from tools.technical import compute_technical_indicators

data = fetch_stock_data("AAPL")

technical = compute_technical_indicators(data["historical_data"])

print("Technical Analysis:")
print(technical)
