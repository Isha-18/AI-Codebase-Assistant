import logging
from time import perf_counter

from langchain.tools import tool

from services.repository_service import RepositoryService


logger = logging.getLogger(__name__)

repository_service = RepositoryService()


def _log_tool_result(
    tool_name: str,
    start: float,
    result_size: int,
):

    elapsed_ms = (
        perf_counter() - start
    ) * 1000

    logger.info(
        "tool=%s event=completed "
        "latency_ms=%.2f result_size=%d",
        tool_name,
        elapsed_ms,
        result_size,
    )


@tool
def list_classes() -> str:
    """
    Returns all classes in the indexed repository.
    """

    start = perf_counter()

    logger.info(
        "tool=list_classes event=started"
    )

    try:

        classes = (
            repository_service
            .get_classes()
        )

    except Exception:

        logger.exception(
            "tool=list_classes event=failed "
            "latency_ms=%.2f",
            (
                perf_counter()
                - start
            ) * 1000,
        )

        raise

    if not classes:
        result = "No classes found."
    else:
        result = "\n".join(classes)

    _log_tool_result(
        "list_classes",
        start,
        len(classes),
    )

    return result


@tool
def list_functions() -> str:
    """
    Returns all functions in the indexed repository.
    """

    start = perf_counter()

    logger.info(
        "tool=list_functions event=started"
    )

    try:

        functions = (
            repository_service
            .get_functions()
        )

    except Exception:

        logger.exception(
            "tool=list_functions event=failed "
            "latency_ms=%.2f",
            (
                perf_counter()
                - start
            ) * 1000,
        )

        raise

    if not functions:
        result = "No functions found."
    else:
        result = "\n".join(functions)

    _log_tool_result(
        "list_functions",
        start,
        len(functions),
    )

    return result


@tool
def list_imports() -> str:
    """
    Returns all imported modules.
    """

    start = perf_counter()

    logger.info(
        "tool=list_imports event=started"
    )

    try:

        imports = (
            repository_service
            .get_imports()
        )

    except Exception:

        logger.exception(
            "tool=list_imports event=failed "
            "latency_ms=%.2f",
            (
                perf_counter()
                - start
            ) * 1000,
        )

        raise

    if not imports:
        result = "No imports found."
    else:
        result = "\n".join(imports)

    _log_tool_result(
        "list_imports",
        start,
        len(imports),
    )

    return result


@tool
def repository_statistics() -> str:
    """
    Returns repository statistics.
    """

    start = perf_counter()

    logger.info(
        "tool=repository_statistics event=started"
    )

    try:

        stats = (
            repository_service
            .get_stats()
        )

    except Exception:

        logger.exception(
            "tool=repository_statistics "
            "event=failed latency_ms=%.2f",
            (
                perf_counter()
                - start
            ) * 1000,
        )

        raise

    result = (
        f"Documents : "
        f"{stats['total_documents']}\n"
        f"Classes : "
        f"{stats['total_classes']}\n"
        f"Functions : "
        f"{stats['total_functions']}"
    )

    _log_tool_result(
        "repository_statistics",
        start,
        len(result),
    )

    return result