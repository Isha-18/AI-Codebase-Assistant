from mcp.server.fastmcp import FastMCP

from services.chat_service import ChatService
from services.repository_service import RepositoryService
from services.indexing_service import IndexingService


chat_service = ChatService()
repository_service = RepositoryService()
indexing_service = IndexingService()


def register_tools(mcp: FastMCP):
    """
    Register all MCP tools.

    Tools expose actions that AI clients can execute.
    """

    @mcp.tool(
        name="chat_repository",
        description="Ask questions about the indexed repository."
    )
    def chat_repository(question: str) -> dict:
        """
        Chat with the indexed repository.
        """

        return chat_service.chat(question)

    @mcp.tool(
        name="list_classes",
        description="Return all classes present in the repository."
    )
    def list_classes() -> list[str]:

        return repository_service.get_classes()

    @mcp.tool(
        name="list_functions",
        description="Return all functions present in the repository."
    )
    def list_functions() -> list[str]:

        return repository_service.get_functions()

    @mcp.tool(
        name="list_imports",
        description="Return all imports present in the repository."
    )
    def list_imports() -> list[str]:

        return repository_service.get_imports()

    @mcp.tool(
        name="repository_statistics",
        description="Return repository statistics."
    )
    def repository_statistics() -> dict:

        return repository_service.get_stats()

    @mcp.tool(
        name="index_repository",
        description="Index a repository from the given local path."
    )
    def index_repository(repository_path: str) -> dict:

        chunks = indexing_service.index_repository(
            repository_path
        )

        return {
            "status": "success",
            "chunks_indexed": chunks
        }