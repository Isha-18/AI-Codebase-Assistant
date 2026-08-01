from llm.llm import llm
from graph.tool_registry import TOOLS

graph_llm = llm.bind_tools(TOOLS)