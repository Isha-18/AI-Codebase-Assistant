from fastapi import APIRouter

from core.loader import load_repository
from core.chunker import chunk_documents
from core.vectorstore import create_vectorstore
from core.rag import ask_question

router = APIRouter()


@router.post("/index")
def index_repository(repository_path: str):

    documents = load_repository(repository_path)

    chunks = chunk_documents(documents)

    create_vectorstore(chunks)

    return {
        "message": "Repository indexed successfully!"
    }


@router.get("/chat")
def chat(question: str):

    response = ask_question(question)

    return {
        "answer": response
    }