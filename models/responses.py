from typing import Any, List, Literal

from pydantic import BaseModel


class IndexResponse(BaseModel):
    message: str
    chunks: int


class ChatResponse(BaseModel):
    status: Literal[
        "completed",
        "approval_required",
    ]

    answer: str | None = None

    sources: List[str] = []

    approval_request: dict[str, Any] | None = None