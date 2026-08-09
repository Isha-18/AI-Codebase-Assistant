import logging

from langchain_core.messages import SystemMessage
from langgraph.graph import END, START, StateGraph

from graph.llm import supervisor_llm
from graph.state import AgentState


logger = logging.getLogger(__name__)


SUPERVISOR_SYSTEM_PROMPT = """
You are the supervisor of an AI Codebase Assistant.

You must decide which specialized agent should handle
the user's request.

Available agents:

1. repository
   Use for:
   - listing classes
   - listing functions
   - listing imports
   - repository statistics
   - indexing a repository
   - repository structure or metadata

2. rag
   Use for:
   - understanding code
   - explaining implementation
   - answering questions about how code works
   - finding relevant code and explaining it
   - reasoning over the repository

Return ONLY one word:

repository

or

rag
"""


def supervisor_node(
    state: AgentState,
):

    messages = state.get(
        "messages",
        [],
    )

    logger.info(
        "agent=supervisor event=started "
        "message_count=%d",
        len(messages),
    )

    supervisor_messages = [
        SystemMessage(
            content=SUPERVISOR_SYSTEM_PROMPT
        ),
        *messages,
    ]

    response = supervisor_llm.invoke(
        supervisor_messages
    )

    decision = (
        response.content
        .strip()
        .lower()
    )

    logger.info(
        "agent=supervisor event=decision "
        "decision=%s",
        decision,
    )

    if "repository" in decision:
        route = "repository"

    elif "rag" in decision:
        route = "rag"

    else:
        logger.warning(
            "agent=supervisor event=invalid_decision "
            "response=%s",
            response.content,
        )

        # Safe fallback.
        route = "rag"

    return {
        "agent_route": route,
    }


def route_from_supervisor(
    state: AgentState,
):

    route = state.get(
        "agent_route"
    )

    if route == "repository":
        return "repository"

    return "rag"


def build_supervisor_graph(
    repository_agent,
    rag_agent,
):

    workflow = StateGraph(
        AgentState
    )

    workflow.add_node(
        "supervisor",
        supervisor_node,
    )

    workflow.add_node(
        "repository",
        repository_agent,
    )

    workflow.add_node(
        "rag",
        rag_agent,
    )

    workflow.add_edge(
        START,
        "supervisor",
    )

    workflow.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "repository": "repository",
            "rag": "rag",
        },
    )

    workflow.add_edge(
        "repository",
        END,
    )

    workflow.add_edge(
        "rag",
        END,
    )

    return workflow