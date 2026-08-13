from graph.agents.rag_agent import (
    build_rag_agent,
)

from graph.agents.repository_agent import (
    build_repository_agent,
)

from graph.agents.code_review_agent import (
    build_code_review_agent,
)

from graph.agents.supervisor import (
    build_supervisor_graph,
)

from graph.memory import memory


repository_agent = (
    build_repository_agent()
)

rag_agent = (
    build_rag_agent()
)

code_review_agent = (
    build_code_review_agent()
)


workflow = build_supervisor_graph(
    repository_agent=repository_agent,
    rag_agent=rag_agent,
    code_review_agent=code_review_agent,
)


graph = workflow.compile(
    checkpointer=memory
)