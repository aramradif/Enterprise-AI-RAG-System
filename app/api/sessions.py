from fastapi import APIRouter, HTTPException, status

from app.models.session import (
    SessionDetail,
    SessionSummary,
)
from app.services.session_registry import session_service


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)


@router.post(
    "",
    response_model=SessionSummary,
    status_code=status.HTTP_201_CREATED,
)
def create_session():
    """
    Create a new conversation session.
    """

    return session_service.create_session()


@router.get(
    "",
    response_model=list[SessionSummary],
)
def list_sessions():
    """
    Return all conversation sessions.
    """

    return session_service.list_sessions()


@router.get(
    "/{session_id}",
    response_model=SessionDetail,
)
def get_session(
    session_id: str,
):
    """
    Return one session and its complete message history.
    """

    session = session_service.get_session(
        session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )

    return session


@router.delete(
    "/{session_id}/messages",
    status_code=status.HTTP_204_NO_CONTENT,
)
def clear_session_messages(
    session_id: str,
):
    """
    Clear all messages from one session
    while keeping the session itself.
    """

    cleared = session_service.clear_session(
        session_id,
    )

    if not cleared:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_session(
    session_id: str,
):
    """
    Permanently remove one in-memory session.
    """

    deleted = session_service.delete_session(
        session_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )