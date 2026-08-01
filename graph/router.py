class Router:

    @staticmethod
    def execute(state):

        print("\n========== LLM INPUT ==========")
        print(state["messages"])

        response = graph_llm.invoke(
            state["messages"]
        )

        print("\n========== LLM RESPONSE ==========")
        print(response)

        print("\n========== TOOL CALLS ==========")
        print(response.tool_calls)

        return {
            "messages": [response]
        }