# test_agent.py — full agent pipeline test
from agent.graph import build_graph

agent = build_graph()

queries = [
    "Analyze AAPL",
    "Compare AAPL and MSFT",
    "What is the Sharpe Ratio?",
]

for query in queries:
    print(f"\n{'='*50}")
    print(f"Query: {query}")
    print("="*50)
    result = agent.invoke({"user_query": query})
    print(result["final_output"])
