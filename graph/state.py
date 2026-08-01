from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    Shared graph state.
    """

    messages: Annotated[list[BaseMessage], add_messages]