import logging

from langgraph.graph import (
    END,
    START,
    StateGraph,
)
from langgraph.prebuilt import ToolNode

from graph.llm import rag_llm
from graph.state import AgentState
from graph.tool_registry import RAG_TOOLS


logger = logging.getLogger(__name__)


rag_tool_node = ToolNode(
    RAG_TOOLS
)


def rag_llm_node(state: AgentState):

    messages = state.get(
        "messages",
        [],
    )

    logger.info(
        "agent=rag event=llm_started "
        "message_count=%d",
        len(messages),
    )

    response = rag_llm.invoke(
        messages
    )

    logger.info(
        "agent=rag event=llm_completed "
        "tool_calls=%s",
        [
            call.get("name")
            for call in (
                getattr(
                    response,
                    "tool_calls",
                    [],
                )
                or []
            )
        ],
    )

    return {
        "messages": [response]
    }


def route_after_rag_llm(
    state: AgentState,
):

    messages = state.get(
        "messages",
        [],
    )

    if not messages:
        return END

    last_message = messages[-1]

    tool_calls = (
        getattr(
            last_message,
            "tool_calls",
            [],
        )
        or []
    )

    if tool_calls:
        return "tools"

    return END


def build_rag_agent():

    workflow = StateGraph(
        AgentState
    )

    workflow.add_node(
        "rag_llm",
        rag_llm_node,
    )

    workflow.add_node(
        "rag_tools",
        rag_tool_node,
    )

    workflow.add_edge(
        START,
        "rag_llm",
    )

    workflow.add_conditional_edges(
        "rag_llm",
        route_after_rag_llm,
        {
            "tools": "rag_tools",
            END: "rag_complete",
        },
    )

    workflow.add_node(
        "rag_complete",
        rag_agent_complete,
)

    workflow.add_edge(
        "rag_complete",
        END,
)

    workflow.add_edge(
        "rag_tools",
        "rag_llm",
    )

    return workflow.compile()

def rag_agent_complete(state: AgentState):
    """
    Store the RAG agent's result and return
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

    agent_results["rag"] = result

    return {
        "agent_results": agent_results,
        "current_agent": "rag",
        "continue_workflow": True,
    }