
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

    review_type: str | None

    # Results produced by specialized agents.
    agent_results: dict[str, Any]

    # Agent currently responsible for the task.
    current_agent: str | None

    # Number of agent transitions performed.
    agent_iterations: int

    # Prevents agents from looping indefinitely.
    max_agent_iterations: int

