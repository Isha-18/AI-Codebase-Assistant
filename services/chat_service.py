import logging
from time import perf_counter

from langchain_core.messages import HumanMessage
from langgraph.types import Command

from graph import graph


logger = logging.getLogger(__name__)


def _get_interrupt_payload(result):

    interrupts = result.get(
        "__interrupt__"
    )

    if not interrupts:
        return None

    interrupt = interrupts[0]

    return getattr(
        interrupt,
        "value",
        interrupt,
    )


class ChatService:

    def _config(
        self,
        thread_id: str,
        run_name: str,
    ):

        return {
            "configurable": {
                "thread_id": thread_id
            },
            "run_name": run_name,
            "tags": [
                "chat",
                "langgraph",
                "codebase-assistant",
            ],
            "metadata": {
                "thread_id": thread_id,
            },
        }

    def chat(
        self,
        question: str,
        thread_id: str,
    ):

        start = perf_counter()

        logger.info(
            "chat event=request_started "
            "thread_id=%s question=%s",
            thread_id,
            question,
        )

        config = self._config(
            thread_id,
            "codebase_chat",
        )

        try:

            result = graph.invoke(
                {
                "messages": [
                    HumanMessage(
                        content=question
                    )
                ],
                "agent_results": {},
                "agent_iterations": 0,
                "max_agent_iterations": 3,
                "current_agent": None,
                "agent_route": None,
                "continue_workflow": False,
                "workflow_complete": False,
            },
            config=config,
)

        except Exception:

            elapsed_ms = (
                perf_counter() - start
            ) * 1000

            logger.exception(
                "chat event=request_failed "
                "thread_id=%s latency_ms=%.2f",
                thread_id,
                elapsed_ms,
            )

            raise

        approval_request = (
            _get_interrupt_payload(
                result
            )
        )

        if approval_request:

            logger.info(
                "chat event=approval_required "
                "thread_id=%s",
                thread_id,
            )

            return {
                "status": "approval_required",
                "answer": None,
                "sources": [],
                "approval_request": (
                    approval_request
                ),
            }

        elapsed_ms = (
            perf_counter() - start
        ) * 1000

        answer = (
            result["messages"][-1]
            .content
        )

        logger.info(
            "chat event=request_completed "
            "thread_id=%s latency_ms=%.2f",
            thread_id,
            elapsed_ms,
        )

        return {
            "status": "completed",
            "answer": answer,
            "sources": [],
            "approval_request": None,
        }

    def approve(
        self,
        thread_id: str,
        approved: bool,
    ):

        start = perf_counter()

        logger.info(
            "chat event=approval_submitted "
            "thread_id=%s approved=%s",
            thread_id,
            approved,
        )

        config = self._config(
            thread_id,
            "codebase_chat_resume",
        )

        try:

            result = graph.invoke(
                Command(
                    resume={
                        "approved": approved
                    }
                ),
                config=config,
            )

        except Exception:

            elapsed_ms = (
                perf_counter() - start
            ) * 1000

            logger.exception(
                "chat event=resume_failed "
                "thread_id=%s latency_ms=%.2f",
                thread_id,
                elapsed_ms,
            )

            raise

        approval_request = (
            _get_interrupt_payload(
                result
            )
        )

        if approval_request:

            logger.info(
                "chat event=approval_required_again "
                "thread_id=%s",
                thread_id,
            )

            return {
                "status": "approval_required",
                "answer": None,
                "sources": [],
                "approval_request": (
                    approval_request
                ),
            }

        elapsed_ms = (
            perf_counter() - start
        ) * 1000

        answer = (
            result["messages"][-1]
            .content
        )

        logger.info(
            "chat event=request_completed_after_approval "
            "thread_id=%s latency_ms=%.2f",
            thread_id,
            elapsed_ms,
        )

        return {
            "status": "completed",
            "answer": answer,
            "sources": [],
            "approval_request": None,
        }

    def stream(
        self,
        question: str,
        thread_id: str,
    ):

        config = self._config(
            thread_id,
            "codebase_chat_debug",
        )

        state = {
            "messages": [
                HumanMessage(
                    content=question
                )
            ]
        }

        logger.info(
            "chat event=debug_stream_started "
            "thread_id=%s question=%s",
            thread_id,
            question,
        )

        try:

            for event in graph.stream(
                state,
                config=config,
                stream_mode="debug",
            ):
                yield event

        except Exception:

            logger.exception(
                "chat event=debug_stream_failed "
                "thread_id=%s",
                thread_id,
            )

            raise

    async def response_stream(
        self,
        question: str,
        thread_id: str,
    ):

        state = {
            "messages": [
                HumanMessage(
                    content=question
                )
            ]
        }

        config = self._config(
            thread_id,
            "codebase_chat_stream",
        )

        logger.info(
            "chat event=response_stream_started "
            "thread_id=%s question=%s",
            thread_id,
            question,
        )

        try:

            async for event in graph.astream_events(
                state,
                config=config,
                version="v2",
            ):

                if (
                    event["event"]
                    != "on_chat_model_stream"
                ):
                    continue

                chunk = event["data"]["chunk"]

                if chunk.content:
                    yield chunk.content

        except Exception:

            logger.exception(
                "chat event=response_stream_failed "
                "thread_id=%s",
                thread_id,
            )

            raise