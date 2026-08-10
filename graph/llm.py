from llm.llm import llm

from graph.tool_registry import (
    RAG_TOOLS,
    REPOSITORY_TOOLS,
    REVIEW_TOOLS
)


repository_llm = llm.bind_tools(
    REPOSITORY_TOOLS
)


rag_llm = llm.bind_tools(
    RAG_TOOLS
)

review_llm = llm.bind_tools(
    REVIEW_TOOLS
)


supervisor_llm = llm