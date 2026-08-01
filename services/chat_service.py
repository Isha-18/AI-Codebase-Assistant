from langchain_core.messages import HumanMessage

from graph import graph


class ChatService:

    def chat(
        self,
        question: str,
        thread_id: str,
    ):

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=question
                    )
                ]
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            },
        )

        return {
            "answer": result["messages"][-1].content,
            "sources": [],
        }