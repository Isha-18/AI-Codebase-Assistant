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

3. code_review
   Use for:
   - reviewing code quality
   - SOLID principle analysis
   - architecture review
   - identifying code smells
   - maintainability analysis
   - refactoring suggestions

Return ONLY one word:

repository

or

rag

or

code_review
"""


VALID_ROUTES = {
    "repository",
    "rag",
    "code_review",
}


def supervisor_node(
    state: AgentState,
):
    messages = state.get(
        "messages",
        [],
    )

    iterations = state.get(
        "agent_iterations",
        0,
    )

    max_iterations = state.get(
        "max_agent_iterations",
        3,
    )

    logger.info(
        "agent=supervisor event=started "
        "message_count=%d iterations=%d/%d",
        len(messages),
        iterations,
        max_iterations,
    )

    # Safety protection against endless agent loops.
    if iterations >= max_iterations:
        logger.warning(
            "agent=supervisor event=max_iterations_reached "
            "iterations=%d",
            iterations,
        )

        return {
            "agent_route": None,
            "current_agent": None,
        }

    supervisor_messages = [
        SystemMessage(
            content=SUPERVISOR_SYSTEM_PROMPT
        ),
        *messages,
    ]

    try:
        response = supervisor_llm.invoke(
            supervisor_messages
        )

    except Exception:
        logger.exception(
            "agent=supervisor event=failed"
        )

        # Keep the existing safe fallback.
        route = "rag"

    else:
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

        route = None

        for candidate in VALID_ROUTES:
            if candidate in decision:
                route = candidate
                break

        if route is None:
            logger.warning(
                "agent=supervisor event=invalid_decision "
                "response=%s",
                response.content,
            )

            route = "rag"

    logger.info(
        "agent=supervisor event=route_selected "
        "route=%s",
        route,
    )

    return {
        "agent_route": route,
        "current_agent": route,
        "agent_iterations": iterations + 1,
    }


def route_from_supervisor(
    state: AgentState,
):
    route = state.get(
        "agent_route"
    )

    if route == "repository":
        return "repository"

    if route == "code_review":
        return "code_review"

    if route == "rag":
        return "rag"

    return END


def build_supervisor_graph(
    repository_agent,
    rag_agent,
    code_review_agent,
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

    workflow.add_node(
        "code_review",
        code_review_agent,
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
            "code_review": "code_review",
            END: END,
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

    workflow.add_edge(
        "code_review",
        END,
    )

    return workflow

