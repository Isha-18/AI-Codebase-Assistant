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
                    HumanMessage(content=question)
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

    def stream(
        self,
        question: str,
        thread_id: str,
    ):

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        state = {
            "messages": [
                HumanMessage(content=question)
            ]
        }

        for event in graph.stream(
            state,
            config=config,
            stream_mode="updates",
        ):
            yield event

    async def response_stream(
    self,
    question: str,
    thread_id: str,
):

        state = {
            "messages": [
                HumanMessage(content=question)
            ]
        }

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        async for event in graph.astream_events(
        state,
        config=config,
        version="v2",
    ):

            if event["event"] != "on_chat_model_stream":
                continue

            chunk = event["data"]["chunk"]

            if chunk.content:
                yield chunk.content

    