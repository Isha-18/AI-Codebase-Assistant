from langchain_chroma import Chroma

from config.settings import settings
from indexing.embeddings import embeddings


def get_retriever():
    """
    Retrieve a larger candidate set.
    RAGService will rerank these results using
    code-aware metadata matching.
    """

    vectorstore = Chroma(
        persist_directory=str(settings.CHROMA_DB_PATH),
        embedding_function=embeddings,
    )

    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": settings.RETRIEVAL_RERANK_CANDIDATES,
            "fetch_k": settings.RETRIEVAL_FETCH_K,
            "lambda_mult": 0.7,
        },
    )