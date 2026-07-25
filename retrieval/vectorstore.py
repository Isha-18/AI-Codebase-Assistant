from langchain_chroma import Chroma

from core.embeddings import embeddings


VECTOR_DB_PATH = "storage/chroma_db"


def create_vectorstore(documents):
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )

    return vectorstore