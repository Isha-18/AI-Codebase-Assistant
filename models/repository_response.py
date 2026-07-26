from typing import List

from pydantic import BaseModel


class RepositoryClassesResponse(BaseModel):
    classes: List[str]


class RepositoryFunctionsResponse(BaseModel):
    functions: List[str]


class RepositoryImportsResponse(BaseModel):
    imports: List[str]


class RepositoryStatsResponse(BaseModel):
    total_documents: int
    total_classes: int
    total_functions: int