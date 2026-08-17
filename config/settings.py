from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    """Application configuration."""

    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    # Repository
    REPOSITORY_PATH = PROJECT_ROOT / "data" / "repository"

    # Storage
    CHROMA_DB_PATH = PROJECT_ROOT / "storage" / "chroma_db"

    # Embeddings
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "BAAI/bge-small-en-v1.5",
    )

    # LLM
    LLM_MODEL = os.getenv(
        "LLM_MODEL",
        "qwen3:4b",
    )

    # Retrieval
    RETRIEVAL_TOP_K = int(
        os.getenv("RETRIEVAL_TOP_K", "5")
    )

    RETRIEVAL_FETCH_K = int(
        os.getenv("RETRIEVAL_FETCH_K", "15")
    )

    RETRIEVAL_RERANK_CANDIDATES = int(
        os.getenv("RETRIEVAL_RERANK_CANDIDATES", "10")
    )

    # Chunking
    CHUNK_SIZE = int(
        os.getenv("CHUNK_SIZE", "1000")
    )

    CHUNK_OVERLAP = int(
        os.getenv("CHUNK_OVERLAP", "200")
    )

    # LangSmith observability
    LANGSMITH_TRACING = os.getenv(
        "LANGSMITH_TRACING",
        "false",
    ).lower() == "true"

    LANGSMITH_PROJECT = os.getenv(
        "LANGSMITH_PROJECT",
        "ai-codebase-assistant",
    )

    LANGSMITH_ENDPOINT = os.getenv(
        "LANGSMITH_ENDPOINT",
        "https://api.smith.langchain.com",
    )


settings = Settings()