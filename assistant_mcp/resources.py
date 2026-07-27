from pathlib import Path

from mcp.server.fastmcp import FastMCP

from services.repository_service import RepositoryService


repository_service = RepositoryService()


def register_resources(mcp: FastMCP):
    """
    Register all MCP resources.

    Resources expose read-only information about
    the indexed repository.
    """

    @mcp.resource("repository://statistics")
    def repository_statistics() -> dict:
        """
        Repository statistics.
        """
        return repository_service.get_stats()

    @mcp.resource("repository://classes")
    def repository_classes() -> list[str]:
        """
        List all classes.
        """
        return repository_service.get_classes()

    @mcp.resource("repository://functions")
    def repository_functions() -> list[str]:
        """
        List all functions.
        """
        return repository_service.get_functions()

    @mcp.resource("repository://imports")
    def repository_imports() -> list[str]:
        """
        List all imports.
        """
        return repository_service.get_imports()

    @mcp.resource("repository://readme")
    def repository_readme() -> str:
        """
        Returns the repository README if available.
        """

        readme = Path("README.md")

        if readme.exists():
            return readme.read_text(encoding="utf-8")

        return "README.md not found."

    @mcp.resource("repository://architecture")
    def repository_architecture() -> str:
        """
        Returns a simple overview of the project architecture.
        """

        return """
AI-Codebase-Assistant

api/
analyzers/
config/
indexing/
llm/
models/
mcp/
prompts/
retrieval/
services/
storage/
tools/

Architecture Flow

Client
↓

FastAPI / MCP

↓

Services

↓

Retrieval

↓

Vector Store

↓

LLM
"""