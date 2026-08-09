import logging
from time import perf_counter

from langchain.tools import tool

from services.rag_service import RAGService


logger = logging.getLogger(__name__)

rag_service = RAGService()


@tool
def codebase_chat(question: str) -> str:
    """
    Use this tool whenever the user asks about:

    - how the code works
    - authentication
    - APIs
    - repository architecture
    - implementation details
    - explain code
    - summarize files
    - code flow
    - debugging
    - repository questions

    Never answer these questions from your own knowledge.
    Always search the repository first.
    """

    start = perf_counter()

    logger.info(
        "tool=codebase_chat event=started question=%s",
        question,
    )

    try:

        result = rag_service.chat(
            question
        )

    except Exception:

        elapsed_ms = (
            perf_counter() - start
        ) * 1000

        logger.exception(
            "tool=codebase_chat event=failed "
            "latency_ms=%.2f",
            elapsed_ms,
        )

        raise

    elapsed_ms = (
        perf_counter() - start
    ) * 1000

    logger.info(
        "tool=codebase_chat event=completed "
        "latency_ms=%.2f sources=%d",
        elapsed_ms,
        len(
            result.get(
                "sources",
                [],
            )
        ),
    )

    return result["answer"]