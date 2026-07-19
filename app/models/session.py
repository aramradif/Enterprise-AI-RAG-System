from datetime import datetime

from pydantic import BaseModel, Field

from app.models.chat import ChatMessage


class SessionSummary(BaseModel):
    """
    Summary information displayed in the
    Enterprise Sessions Dashboard.
    """

    session_id: str

    message_count: int = Field(
        default=0,
        ge=0,
    )

    created_at: datetime
    last_active_at: datetime


class SessionDetail(SessionSummary):
    """
    Complete session information including
    the conversation history.
    """

    messages: list[ChatMessage]