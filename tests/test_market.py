from tools.market_data import fetch_stock_data

data = fetch_stock_data("AAPL")

print("Ticker:", data["ticker"])
print("Current Price:", data["current_price"])
print("PE Ratio:", data["pe_ratio"])
print("Market Cap:", data["market_cap"])
print("Historical Data Head:")
print(data["historical_data"].head())
