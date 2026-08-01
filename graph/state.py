from typing import Annotated, TypedDict

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    Shared state passed between every node.
    """

    messages: Annotated[list[BaseMessage], add_messages]

    question: str

    selected_tool: str

    retrieved_docs: list[Document]

    tool_result: str

    final_response: str

    metadata: dict