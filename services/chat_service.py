from langchain_core.messages import HumanMessage

from graph import graph


class ChatService:

    def chat(self, question: str):

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=question)
                ]
            }
        )

        return result["messages"][-1].content