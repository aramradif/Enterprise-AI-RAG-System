from app.memory.conversation_manager import ConversationManager


class SessionManager:
    """
    Manages multiple conversations.

    One ConversationManager per session.
    """

    def __init__(self):
        self.sessions = {}

    def get_conversation(
        self,
        session_id: str,
    ):
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationManager()

        return self.sessions[session_id]

    def clear(
        self,
        session_id: str,
    ):
        if session_id in self.sessions:
            self.sessions[session_id].clear()