import logging
from time import perf_counter

from langchain.tools import tool

from services.indexing_service import IndexingService


logger = logging.getLogger(__name__)

indexing_service = IndexingService()


@tool
def index_repository(repository_path: str) -> str:
    """
    Index a repository into the codebase assistant.

    Use this when the user explicitly asks to index,
    re-index, or add a repository.

    The operation changes repository/vector-store state
    and therefore requires human approval before execution.
    """

    start = perf_counter()

    logger.info(
        "tool=index_repository event=started "
        "repository_path=%s",
        repository_path,
    )

    try:

        chunks = (
            indexing_service.index_repository(
                repository_path
            )
        )

    except Exception:

        elapsed_ms = (
            perf_counter() - start
        ) * 1000

        logger.exception(
            "tool=index_repository event=failed "
            "latency_ms=%.2f",
            elapsed_ms,
        )

        raise

    elapsed_ms = (
        perf_counter() - start
    ) * 1000

    logger.info(
        "tool=index_repository event=completed "
        "latency_ms=%.2f chunks=%d",
        elapsed_ms,
        chunks,
    )

    return (
        f"Repository indexed successfully. "
        f"Chunks indexed: {chunks}"
    )