from app.models.chat import ChatMessage


class ConversationMemory:
    """
    Simple in-memory conversation history.

    Will later be replaced with Redis,
    CosmosDB,
    PostgreSQL,
    etc.
    """

    def __init__(self):
        self.messages = []

    def add(
        self,
        role: str,
        content: str,
    ):
        self.messages.append(
            ChatMessage(
                role=role,
                content=content,
            )
        )

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []