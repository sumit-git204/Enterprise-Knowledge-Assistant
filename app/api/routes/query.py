from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.api.dependencies import get_rag_service
from app.services.rag_services import RAGService

router = APIRouter()


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)
    source: str | None = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[dict]


@router.post("/query", response_model=QueryResponse)
def query_knowledge(
    request: QueryRequest,
    rag_service: RAGService = Depends(get_rag_service),
):
    try:
        return rag_service.ask(
            question=request.question,
            top_k=request.top_k,
            source=request.source,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc