import logging

from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode

from graph.state import AgentState
from graph.llm import review_llm
from graph.tool_registry import REVIEW_TOOLS

logger = logging.getLogger(__name__)

review_tools = ToolNode(REVIEW_TOOLS)


def review_llm_node(state):

    logger.info(
        "agent=code_review event=started"
    )

    response = review_llm.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


def review_route(state):

    last = state["messages"][-1]

    if getattr(last, "tool_calls", None):
        return "tools"

    return END


def build_code_review_agent():

    workflow = StateGraph(AgentState)

    workflow.add_node(
        "llm",
        review_llm_node,
    )

    workflow.add_node(
        "tools",
        review_tools,
    )

    workflow.add_edge(
        START,
        "llm",
    )

    workflow.add_conditional_edges(
        "llm",
        review_route,
        {
            "tools": "tools",
            END: END,
        },
    )

    workflow.add_edge(
        "tools",
        "llm",
    )

    return workflow.compile()