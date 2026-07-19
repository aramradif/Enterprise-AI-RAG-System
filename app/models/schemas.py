from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """
    Request body used by the RAG endpoints.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="The user's question.",
    )

    session_id: str = Field(
        default="default",
        min_length=1,
        description=(
            "Conversation session identifier. "
            "Requests without a session ID use the default session."
        ),
    )


class AnswerResponse(BaseModel):
    """
    Standard non-streaming answer response.
    """

    answer: str