from langchain_chroma import Chroma

from core.embeddings import embeddings


VECTOR_DB_PATH = "storage/chroma_db"


def get_retriever():
    vectorstore = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    return vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )