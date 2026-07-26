from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config.settings import settings


embeddings = HuggingFaceEmbeddings(
    model_name=settings.EMBEDDING_MODEL
)


def create_vectorstore(documents):

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=settings.CHROMA_DB_PATH,
    )

    return vectorstore


def get_vectorstore():

    return Chroma(
        persist_directory=settings.CHROMA_DB_PATH,
        embedding_function=embeddings,
    )