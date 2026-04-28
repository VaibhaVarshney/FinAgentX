from typing import TypedDict, Optional


class AgentState(TypedDict):
    user_query: str
    ticker: Optional[str]
    intent: Optional[str]
    analysis_result: Optional[dict]
    final_output: Optional[str]
