from typing import TypedDict, Optional


class AgentState(TypedDict):
    user_query: str
    ticker: Optional[str]
    intent: Optional[str]
    analysis_result: Optional[dict]
    # stores [analysis1, analysis2] for comparison
    comparison_results: Optional[list]
    final_output: Optional[str]
