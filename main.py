from agent.graph import build_graph


def main():
    agent = build_graph()

    print("=" * 50)
    print("  FinAgentX — Educational Finance Agent")
    print("  Powered by Groq (llama3-8b-8192)")
    print("=" * 50)
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            result = agent.invoke({"user_query": user_input})
            print(f"\nAgent:\n{result['final_output']}\n")
            print("-" * 50)
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
