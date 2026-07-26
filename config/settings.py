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

    EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-small-en-v1.5"
)

    LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "qwen2.5:0.5b"
)

    # Chunking
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200


settings = Settings()