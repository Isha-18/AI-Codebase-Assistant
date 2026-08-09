from graph.agents.rag_agent import (
    build_rag_agent,
)

from graph.agents.repository_agent import (
    build_repository_agent,
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


workflow = build_supervisor_graph(
    repository_agent=repository_agent,
    rag_agent=rag_agent,
)


graph = workflow.compile(
    checkpointer=memory
)