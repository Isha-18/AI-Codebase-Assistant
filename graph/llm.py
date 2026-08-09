from llm.llm import llm

from graph.tool_registry import (
    RAG_TOOLS,
    REPOSITORY_TOOLS,
)


repository_llm = llm.bind_tools(
    REPOSITORY_TOOLS
)


rag_llm = llm.bind_tools(
    RAG_TOOLS
)


supervisor_llm = llm