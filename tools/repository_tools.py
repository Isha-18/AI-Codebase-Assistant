from langchain.tools import tool

from services.repository_service import RepositoryService

repository_service = RepositoryService()


@tool
def list_classes() -> str:
    """
    Returns all classes in the indexed repository.
    """

    classes = repository_service.get_classes()

    if not classes:
        return "No classes found."

    return "\n".join(classes)


@tool
def list_functions() -> str:
    """
    Returns all functions in the indexed repository.
    """

    functions = repository_service.get_functions()

    if not functions:
        return "No functions found."

    return "\n".join(functions)


@tool
def list_imports() -> str:
    """
    Returns all imported modules.
    """

    imports = repository_service.get_imports()

    if not imports:
        return "No imports found."

    return "\n".join(imports)


@tool
def repository_statistics() -> str:
    """
    Returns repository statistics.
    """

    stats = repository_service.get_stats()

    return (
        f"Documents : {stats['total_documents']}\n"
        f"Classes : {stats['total_classes']}\n"
        f"Functions : {stats['total_functions']}"
    )