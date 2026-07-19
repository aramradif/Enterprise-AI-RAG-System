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

    Uses session-based conversation memory.
    """

    answer = service.answer(
        question=request.question,
        session_id=request.session_id,
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
    retrieval, latency, token usage,
    cost estimation, and session-aware
    conversation memory.
    """

    return service.answer_with_metrics(
        question=request.question,
        session_id=request.session_id,
    )


@router.post("/ask/stream")
def ask_stream(
    request: QuestionRequest,
):
    """
    Streaming Enterprise RAG endpoint.

    Streams responses while maintaining
    conversation history for the selected session.
    """

    return StreamingResponse(
        service.stream(
            question=request.question,
            session_id=request.session_id,
        ),
        media_type="text/plain",
    )
