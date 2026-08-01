from langgraph.prebuilt import ToolNode

from tools.rag_tools import codebase_chat
from tools.repository_tools import (
    list_classes,
    list_functions,
    list_imports,
    repository_statistics,
)

TOOLS = [
    codebase_chat,
    list_classes,
    list_functions,
    list_imports,
    repository_statistics,
]

tool_node = ToolNode(TOOLS)