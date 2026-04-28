# test_llm.py — tests Groq connection directly
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY"),
)

response = llm.invoke([HumanMessage(content="""
You are an educational financial assistant.
Explain Relative Strength Index (RSI) in stock market analysis.
Include:
- Definition
- What it measures
- Why it matters
""")])

print("\n----- GROQ RESPONSE -----\n")
print(response.content)
