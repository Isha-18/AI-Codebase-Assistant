from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    """
    Shared state for the complete multi-agent workflow.
    """

    messages: Annotated[
        list[BaseMessage],
        add_messages,
    ]

    # Human-in-the-loop state
    approval_status: str | None

    approval_request: dict[str, Any] | None

    # Supervisor routing
    agent_route: str | None

    current_agent: str | None

    # Results returned by completed agents.
    agent_results: dict[str, Any]

    # Multi-agent workflow control.
    agent_iterations: int

    max_agent_iterations: int

    # Whether the current agent has completed
    # and control should return to the supervisor.
    continue_workflow: bool

    # Indicates that the supervisor has decided
    # the overall task is complete.
    workflow_complete: bool