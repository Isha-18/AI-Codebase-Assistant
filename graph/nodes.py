from graph.llm import graph_llm


class RouterNode:

    @staticmethod
    def execute(state):

        print("\n========== ROUTER ==========")

        print(
            state["messages"][-1].content
        )

        return {}


class LLMNode:

    @staticmethod
    def execute(state):

        print("\n========== LLM ==========")

        response = graph_llm.invoke(
            state["messages"]
        )

        print(response)

        return {
            "messages": [response]
        }