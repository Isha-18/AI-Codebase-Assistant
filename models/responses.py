from typing import List

from pydantic import BaseModel


class IndexResponse(BaseModel):
    message: str
    chunks: int


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]