from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas import (
    AnswerResponse,
    QuestionRequest,
)
from app.services.rag_service import RAGService

router = APIRouter()

service = RAGService()


@router.post(
    "/ask",
    response_model=AnswerResponse,
)
def ask(
    request: QuestionRequest,
):
    """
    Standard Enterprise RAG endpoint.
    """

    answer = service.answer(
        request.question,
    )

    return AnswerResponse(
        answer=answer,
    )


@router.post("/evaluate")
def evaluate(
    request: QuestionRequest,
):
    """
    Enterprise evaluation endpoint.

    Returns the answer together with
    retrieval, latency, token, and cost metrics.
    """

    return service.answer_with_metrics(
        request.question,
    )


@router.post("/ask/stream")
def ask_stream(
    request: QuestionRequest,
):
    """
    Streaming Enterprise RAG endpoint.
    """

    return StreamingResponse(
        service.stream(request.question),
        media_type="text/plain",
    )