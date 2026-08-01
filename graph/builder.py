from langgraph.graph import START
from langgraph.graph import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import tools_condition

from graph.nodes import RouterNode, LLMNode
from graph.state import AgentState
from graph.tool_registry import tool_node


class GraphBuilder:

    @staticmethod
    def build():

        workflow = StateGraph(AgentState)

        workflow.add_node(
            "router",
            RouterNode.execute,
        )

        workflow.add_node(
            "llm",
            LLMNode.execute,
        )

        workflow.add_node(
            "tools",
            tool_node,
        )

        workflow.add_edge(
            START,
            "router",
        )

        workflow.add_edge(
            "router",
            "llm",
        )

        workflow.add_conditional_edges(
            "llm",
            tools_condition,
        )

        workflow.add_edge(
            "tools",
            "llm",
        )

        return workflow.compile()