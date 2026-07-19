from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4

from app.memory.conversation_manager import ConversationManager
from app.models.session import (
    SessionDetail,
    SessionSummary,
)


@dataclass
class SessionRecord:
    """
    Internal representation of one conversation session.
    """

    session_id: str
    conversation: ConversationManager
    created_at: datetime
    last_active_at: datetime


class SessionManager:
    """
    Manages multiple in-memory conversation sessions.

    Each session receives its own ConversationManager
    and ConversationMemory instance.
    """

    def __init__(
        self,
        max_history: int = 6,
    ):
        self.max_history = max_history
        self._sessions: dict[str, SessionRecord] = {}
        self._lock = Lock()

    @staticmethod
    def _current_time() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def _generate_session_id() -> str:
        return uuid4().hex[:12]

    def create_session(self) -> SessionSummary:
        """
        Create and register a new conversation session.
        """

        now = self._current_time()
        session_id = self._generate_session_id()

        record = SessionRecord(
            session_id=session_id,
            conversation=ConversationManager(
                max_history=self.max_history,
            ),
            created_at=now,
            last_active_at=now,
        )

        with self._lock:
            self._sessions[session_id] = record

        return self._build_summary(record)

    def get_or_create_session(
        self,
        session_id: str | None = None,
    ) -> SessionRecord:
        """
        Return an existing session or create a new one.

        If a session ID is supplied but does not exist,
        a session is created using that ID.
        """

        with self._lock:
            if session_id and session_id in self._sessions:
                return self._sessions[session_id]

            now = self._current_time()
            resolved_session_id = (
                session_id
                or self._generate_session_id()
            )

            record = SessionRecord(
                session_id=resolved_session_id,
                conversation=ConversationManager(
                    max_history=self.max_history,
                ),
                created_at=now,
                last_active_at=now,
            )

            self._sessions[resolved_session_id] = record

            return record

    def get_conversation(
        self,
        session_id: str,
    ) -> ConversationManager:
        """
        Return the ConversationManager for one session.
        """

        record = self.get_or_create_session(session_id)
        return record.conversation

    def touch_session(
        self,
        session_id: str,
    ) -> None:
        """
        Update the session's last activity timestamp.
        """

        with self._lock:
            record = self._sessions.get(session_id)

            if record is not None:
                record.last_active_at = self._current_time()

    def list_sessions(self) -> list[SessionSummary]:
        """
        Return all sessions ordered by most recent activity.
        """

        with self._lock:
            records = list(self._sessions.values())

        records.sort(
            key=lambda record: record.last_active_at,
            reverse=True,
        )

        return [
            self._build_summary(record)
            for record in records
        ]

    def get_session_detail(
        self,
        session_id: str,
    ) -> SessionDetail | None:
        """
        Return one session and its full message history.
        """

        with self._lock:
            record = self._sessions.get(session_id)

        if record is None:
            return None

        messages = record.conversation.memory.get_messages()

        return SessionDetail(
            session_id=record.session_id,
            message_count=len(messages),
            created_at=record.created_at,
            last_active_at=record.last_active_at,
            messages=messages,
        )

    def clear(
        self,
        session_id: str,
    ) -> bool:
        """
        Clear the conversation history for one session.

        Returns True when the session exists.
        """

        with self._lock:
            record = self._sessions.get(session_id)

        if record is None:
            return False

        record.conversation.clear()
        self.touch_session(session_id)

        return True

    def delete_session(
        self,
        session_id: str,
    ) -> bool:
        """
        Delete one conversation session.

        Returns True when the session existed.
        """

        with self._lock:
            return self._sessions.pop(
                session_id,
                None,
            ) is not None

    @staticmethod
    def _build_summary(
        record: SessionRecord,
    ) -> SessionSummary:
        messages = record.conversation.memory.get_messages()

        return SessionSummary(
            session_id=record.session_id,
            message_count=len(messages),
            created_at=record.created_at,
            last_active_at=record.last_active_at,
        )