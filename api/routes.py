import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models.requests import (
    ApprovalRequest,
    ChatRequest,
    RepositoryRequest,
)
from models.responses import (
    ChatResponse,
    IndexResponse,
)
from models.repository_response import (
    RepositoryClassesResponse,
    RepositoryFunctionsResponse,
    RepositoryImportsResponse,
    RepositoryStatsResponse,
)
from services.chat_service import ChatService
from services.indexing_service import IndexingService
from services.repository_service import RepositoryService


router = APIRouter()

indexing_service = IndexingService()
chat_service = ChatService()
repository_service = RepositoryService()


@router.post(
    "/index",
    response_model=IndexResponse,
)
def index_repository(
    request: RepositoryRequest,
):

    total_chunks = (
        indexing_service.index_repository(
            request.repository_path
        )
    )

    return IndexResponse(
        message="Repository indexed successfully",
        chunks=total_chunks,
    )


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):

    result = chat_service.chat(
        request.question,
        request.thread_id,
    )

    return ChatResponse(
        status=result["status"],
        answer=result["answer"],
        sources=result["sources"],
        approval_request=(
            result["approval_request"]
        ),
    )


@router.post(
    "/chat/approval",
    response_model=ChatResponse,
)
def chat_approval(
    request: ApprovalRequest,
):

    result = chat_service.approve(
        request.thread_id,
        request.approved,
    )

    return ChatResponse(
        status=result["status"],
        answer=result["answer"],
        sources=result["sources"],
        approval_request=(
            result["approval_request"]
        ),
    )


@router.get(
    "/repository/classes",
    response_model=RepositoryClassesResponse,
)
def repository_classes():

    return RepositoryClassesResponse(
        classes=repository_service.get_classes()
    )


@router.get(
    "/repository/functions",
    response_model=RepositoryFunctionsResponse,
)
def repository_functions():

    return RepositoryFunctionsResponse(
        functions=repository_service.get_functions()
    )


@router.get(
    "/repository/imports",
    response_model=RepositoryImportsResponse,
)
def repository_imports():

    return RepositoryImportsResponse(
        imports=repository_service.get_imports()
    )


@router.get(
    "/repository/stats",
    response_model=RepositoryStatsResponse,
)
def repository_stats():

    stats = repository_service.get_stats()

    return RepositoryStatsResponse(
        **stats
    )


@router.post("/chat/debug")
def debug_chat(
    request: ChatRequest,
):

    def generate():

        for event in chat_service.stream(
            request.question,
            request.thread_id,
        ):

            yield (
                json.dumps(
                    event,
                    default=str,
                )
                + "\n"
            )

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
    )


@router.post("/chat/stream")
async def response_stream(
    request: ChatRequest,
):

    return StreamingResponse(
        chat_service.response_stream(
            request.question,
            request.thread_id,
        ),
        media_type="text/plain",
    )