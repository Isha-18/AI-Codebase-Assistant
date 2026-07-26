from indexing.loader import load_repository
from indexing.chunker import chunk_documents
from retrieval.vectorstore import create_vectorstore


class IndexingService:
    """
    Handles the complete indexing workflow.
    """

    def index_repository(self, repository_path: str) -> int:
        """
        Loads, chunks, embeds and stores documents.

        Returns:
            Number of chunks indexed.
        """

        documents = load_repository(repository_path)

        chunks = chunk_documents(documents)

        create_vectorstore(chunks)

        return len(chunks)