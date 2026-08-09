from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    """
    Shared state used by the supervisor and
    specialized agents.
    """

    messages: Annotated[
        list[BaseMessage],
        add_messages,
    ]

    approval_status: str | None

    approval_request: dict[str, Any] | None

    agent_route: str | None