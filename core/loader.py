import os
from langchain_core.documents import Document


# Folders that we do NOT want to index
IGNORE_DIRS = {
    ".git",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".idea",
    ".vscode",
}


def load_repository(repository_path: str):
    """
    Reads all text files from a repository.

    Args:
        repository_path (str):
            Path to the repository.

    Returns:
        list:
            [
                {
                    "path": "...",
                    "content": "..."
                }
            ]
    """

    documents = []

    for root, dirs, files in os.walk(repository_path):

        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for filename in files:

            file_path = os.path.join(root, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as file:

                    documents.append(
                        Document(
                            page_content=file.read(),
                            metadata={
                                "source": file_path
                            }
                        )
                    )
            except Exception:
                # Ignore binary files or unreadable files
                continue

    return documents