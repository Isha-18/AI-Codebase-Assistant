from fastapi import APIRouter

from models.requests import ChatRequest, RepositoryRequest
from models.responses import ChatResponse, IndexResponse
from services.chat_service import ChatService
from services.indexing_service import IndexingService
from services.repository_service import RepositoryService

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
        request.question
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