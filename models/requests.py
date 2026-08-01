from pydantic import BaseModel


class RepositoryRequest(BaseModel):
    repository_path: str


class ChatRequest(BaseModel):
    question: str
    thread_id: str