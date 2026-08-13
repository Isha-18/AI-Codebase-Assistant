from langgraph.graph import (
    StateGraph,
    START,
    END,
)
from langgraph.prebuilt import (
    ToolNode,
)

from graph.state import AgentState
from graph.llm import repository_llm
import logging

from graph.nodes import (
    ApprovalNode,
)

from graph.tool_registry import (
    REPOSITORY_TOOLS,
)

repository_tool_node = ToolNode(
    REPOSITORY_TOOLS
)

logger = logging.getLogger(__name__)

def repository_llm_node(state):

    response = repository_llm.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


def route_after_llm(state):

    messages = state["messages"]

    last_message = messages[-1]

    if getattr(
        last_message,
        "tool_calls",
        None,
    ):
        return "approval"

    return END


def route_after_approval(state):

    status = state.get(
        "approval_status"
    )

    if status == "approved":
        return "tools"

    if status == "rejected":
        return "llm"

    return "tools"


def build_repository_agent():

    workflow = StateGraph(
        AgentState
    )

    workflow.add_node(
        "llm",
        repository_llm_node,
    )

    workflow.add_node(
        "approval",
        ApprovalNode.execute,
    )

    workflow.add_node(
        "tools",
        repository_tool_node,
    )

    workflow.add_node(
        "repository_complete",
        repository_agent_complete,
    )

    workflow.add_edge(
        START,
        "llm",
    )

    workflow.add_conditional_edges(
        "llm",
        route_after_llm,
        {
            "approval": "approval",
            END: "repository_complete",
        },
    )

    workflow.add_conditional_edges(
        "approval",
        route_after_approval,
        {
            "tools": "tools",
            "llm": "llm",
        },
    )

    workflow.add_edge(
        "tools",
        "llm",
    )

    return workflow.compile()

def repository_agent_complete(state: AgentState):
    """
    Store the repository agent's result and return
    control to the Supervisor.
    """

    messages = state.get(
        "messages",
        [],
    )

    result = ""

    if messages:
        result = getattr(
            messages[-1],
            "content",
            "",
        )

    agent_results = dict(
        state.get(
            "agent_results",
            {},
        )
    )

    agent_results["repository"] = result

    return {
        "agent_results": agent_results,
        "current_agent": "repository",
        "continue_workflow": True,
    }

from graph.state import AgentState


def repository_agent_complete(
    state: AgentState,
):
    messages = state.get(
        "messages",
        [],
    )

    result = ""

    if messages:

        result = getattr(
            messages[-1],
            "content",
            "",
        )

    agent_results = dict(
        state.get(
            "agent_results",
            {},
        )
    )

    agent_results["repository"] = result

    logger.info(
        "agent=repository "
        "event=completed "
        "result_size=%d",
        len(str(result)),
    )

    return {
        "agent_results": agent_results,
        "current_agent": "repository",
        "continue_workflow": True,
    }