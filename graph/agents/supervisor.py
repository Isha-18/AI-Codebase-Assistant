import logging

from langchain_core.messages import SystemMessage
from langgraph.graph import END, START, StateGraph

from graph.llm import supervisor_llm
from graph.state import AgentState

logger = logging.getLogger(__name__)


SUPERVISOR_SYSTEM_PROMPT = """
You are the supervisor of an AI Codebase Assistant.

Your job is to decide which specialized agent should handle
the user's request.

Available agents:

repository
- Repository structure
- Classes
- Functions
- Imports
- Repository statistics
- Repository indexing
- Repository metadata

rag
- Understanding code
- Explaining implementation
- Explaining how features work
- Answering questions using repository context
- Finding relevant code

code_review
- Code quality
- SOLID principles
- Architecture review
- Code smells
- Maintainability
- Refactoring suggestions

done
- Use when the task has already been sufficiently completed
- Use when no additional specialized agent is required

IMPORTANT:

If an agent has already produced a useful result, inspect that
result before deciding what should happen next.

A task may require multiple agents.

For example:

"Find the authentication classes and review their architecture."

could require:

repository
then
code_review

Return ONLY one word:

repository
rag
code_review
done
"""


VALID_ROUTES = {
    "repository",
    "rag",
    "code_review",
    "done",
}


def _extract_agent_results(
    state: AgentState,
) -> str:
    """
    Convert previous agent results into compact
    context for the Supervisor.
    """

    results = state.get(
        "agent_results",
        {},
    )

    if not results:
        return "No previous agent results."

    sections = []

    for agent_name, result in results.items():

        sections.append(
            f"""
Agent: {agent_name}

Result:
{result}
"""
        )

    return "\n".join(sections)


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

    # Safety protection.
    if iterations >= max_iterations:

        logger.warning(
            "agent=supervisor "
            "event=max_iterations_reached "
            "iterations=%d",
            iterations,
        )

        return {
            "agent_route": "done",
            "current_agent": None,
            "continue_workflow": False,
            "workflow_complete": True,
        }

    agent_results = _extract_agent_results(
        state
    )

    supervisor_context = f"""
Previous agent results:

{agent_results}

Current agent:
{state.get("current_agent")}

Agent iterations:
{iterations}/{max_iterations}

Based on the original user request and the
previous agent results, decide whether:

1. Another specialized agent is required
OR
2. The task is complete.

Return ONLY one word.
"""

    supervisor_messages = [
        SystemMessage(
            content=(
                SUPERVISOR_SYSTEM_PROMPT
                + "\n"
                + supervisor_context
            )
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

        # Safe fallback.
        route = "done"

    else:

        decision = (
            str(response.content)
            .strip()
            .lower()
        )

        logger.info(
            "agent=supervisor "
            "event=decision "
            "decision=%s",
            decision,
        )

        route = None

        # Check exact words first.
        for candidate in VALID_ROUTES:

            if decision == candidate:

                route = candidate
                break

        # Fallback for models that return
        # additional text.
        if route is None:

            for candidate in VALID_ROUTES:

                if candidate in decision:

                    route = candidate
                    break

        if route is None:

            logger.warning(
                "agent=supervisor "
                "event=invalid_decision "
                "response=%s",
                decision,
            )

            route = "done"

    if route == "done":

        logger.info(
            "agent=supervisor "
            "event=workflow_completed"
        )

        return {
            "agent_route": "done",
            "current_agent": None,
            "continue_workflow": False,
            "workflow_complete": True,
        }

    logger.info(
        "agent=supervisor "
        "event=route_selected "
        "route=%s",
        route,
    )

    return {
        "agent_route": route,
        "current_agent": route,
        "agent_iterations": iterations + 1,
        "continue_workflow": False,
        "workflow_complete": False,
    }


def route_from_supervisor(
    state: AgentState,
):
    route = state.get(
        "agent_route"
    )

    if route == "repository":
        return "repository"

    if route == "rag":
        return "rag"

    if route == "code_review":
        return "code_review"

    if route == "done":
        return END

    return END


def route_after_agent(
    state: AgentState,
):
    """
    Every specialized agent returns control
    to the Supervisor.

    The Supervisor then decides whether another
    agent is required.
    """

    if state.get(
        "workflow_complete",
        False,
    ):
        return END

    return "supervisor"


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

    workflow.add_conditional_edges(
        "repository",
        route_after_agent,
        {
            "supervisor": "supervisor",
            END: END,
        },
    )

    workflow.add_conditional_edges(
        "rag",
        route_after_agent,
        {
            "supervisor": "supervisor",
            END: END,
        },
    )

    workflow.add_conditional_edges(
        "code_review",
        route_after_agent,
        {
            "supervisor": "supervisor",
            END: END,
        },
    )

    return workflow