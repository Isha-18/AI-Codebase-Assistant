from graph.llm import graph_llm


class RouterNode:

    @staticmethod
    def execute(state):

        return {}


class LLMNode:

    @staticmethod
    def execute(state):

        response = graph_llm.invoke(
            state["messages"]
        )

        return {
            "messages": [response]
        }