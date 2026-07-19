from app.memory.session_manager import SessionManager
from app.models.session import (
    SessionDetail,
    SessionSummary,
)


class SessionService:
    """
    Application service for managing conversation sessions.

    This layer sits between the FastAPI endpoints
    and the in-memory SessionManager.
    """

    def __init__(
        self,
        session_manager: SessionManager,
    ):
        self.session_manager = session_manager

    def create_session(self) -> SessionSummary:
        """
        Create and return a new conversation session.
        """

        return self.session_manager.create_session()

    def list_sessions(self) -> list[SessionSummary]:
        """
        Return summaries for all existing sessions.
        """

        return self.session_manager.list_sessions()

    def get_session(
        self,
        session_id: str,
    ) -> SessionDetail | None:
        """
        Return one session with its full conversation history.
        """

        return self.session_manager.get_session_detail(
            session_id,
        )

    def clear_session(
        self,
        session_id: str,
    ) -> bool:
        """
        Clear all messages from one session.
        """

        return self.session_manager.clear(
            session_id,
        )

    def delete_session(
        self,
        session_id: str,
    ) -> bool:
        """
        Permanently remove one in-memory session.
        """

        return self.session_manager.delete_session(
            session_id,
        )