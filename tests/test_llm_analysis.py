from agent.analysis_engine import run_full_stock_analysis
from agent.llm_synthesizer import generate_educational_analysis


data = run_full_stock_analysis("AAPL")

explanation = generate_educational_analysis(data)

print("\nEDUCATIONAL ANALYSIS:\n")
print(explanation)
