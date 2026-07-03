from app.memory.conversation_memory import ConversationMemory
from app.memory.summarizer import ConversationSummarizer


class ConversationManager:
    """
    Enterprise Conversation Manager.
    """

    def __init__(
        self,
        max_history: int = 6,
    ):
        self.memory = ConversationMemory()

        self.summarizer = ConversationSummarizer()

        self.max_history = max_history

    def add_user_message(
        self,
        message: str,
    ):
        self.memory.add(
            role="user",
            content=message,
        )

    def add_assistant_message(
        self,
        message: str,
    ):
        self.memory.add(
            role="assistant",
            content=message,
        )

    def get_history(self):

        messages = self.memory.get_messages()

        return messages[-self.max_history:]

    def get_summary(self):

        return self.summarizer.summarize(
            self.memory.get_messages()
        )

    def clear(self):

        self.memory.clear()