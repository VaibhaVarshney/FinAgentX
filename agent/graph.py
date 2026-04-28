from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.nodes import (
    classify_intent,
    stock_analysis_node,
    concept_explanation_node,
    comparison_node,
)


def route_intent(state: AgentState) -> str:
    intent = state.get("intent", "stock_analysis")

    if intent == "concept_explanation":
        return "concept_explanation"
    if intent == "comparison":
        return "comparison"

    return "stock_analysis"  # default


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("intent_classifier", classify_intent)
    graph.add_node("stock_analysis", stock_analysis_node)
    graph.add_node("concept_explanation", concept_explanation_node)
    graph.add_node("comparison", comparison_node)

    graph.set_entry_point("intent_classifier")

    graph.add_conditional_edges(
        "intent_classifier",
        route_intent,
        {
            "stock_analysis": "stock_analysis",
            "concept_explanation": "concept_explanation",
            "comparison": "comparison",
        }
    )

    graph.add_edge("stock_analysis", END)
    graph.add_edge("concept_explanation", END)
    graph.add_edge("comparison", END)

    return graph.compile()
