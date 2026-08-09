from pydantic import BaseModel


class RepositoryRequest(BaseModel):
    repository_path: str


class ChatRequest(BaseModel):
    question: str
    thread_id: str


class ApprovalRequest(BaseModel):
    thread_id: str
    approved: bool