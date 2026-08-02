from fastapi import APIRouter

from models.requests import ChatRequest, RepositoryRequest
from models.responses import ChatResponse, IndexResponse
from services.chat_service import ChatService
from services.indexing_service import IndexingService
from services.repository_service import RepositoryService
from fastapi.responses import StreamingResponse
import json

from models.repository_response import (
    RepositoryClassesResponse,
    RepositoryFunctionsResponse,
    RepositoryImportsResponse,
    RepositoryStatsResponse,
)


router = APIRouter()

indexing_service = IndexingService()
chat_service = ChatService()


@router.post(
    "/index",
    response_model=IndexResponse
)
def index_repository(request: RepositoryRequest):

    total_chunks = indexing_service.index_repository(
        request.repository_path
    )

    return IndexResponse(
        message="Repository indexed successfully",
        chunks=total_chunks,
    )


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    result = chat_service.chat(
        request.question,
        request.thread_id
    )

    return ChatResponse(
    answer=result["answer"],
    sources=result["sources"],
)

repository_service = RepositoryService()

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

    return RepositoryStatsResponse(**stats)

@router.post("/chat/debug")
def stream_chat(request: ChatRequest):

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
        media_type="application/json",
    )

@router.post("/chat/stream")
async def stream_chat(request: ChatRequest):

    return StreamingResponse(

        chat_service.response_stream(

            request.question,
            request.thread_id,

        ),

        media_type="text/plain",
    )