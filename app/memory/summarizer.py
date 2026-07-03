from app.llm.rag import generate_answer
from app.models.chat import ChatMessage


class ConversationSummarizer:
    """
    GPT-powered Conversation Summarizer.
    """

    def summarize(
        self,
        messages: list[ChatMessage],
    ) -> str:

        if len(messages) <= 6:
            return ""

        conversation = ""

        for message in messages[:-6]:

            conversation += (
                f"{message.role}: {message.content}\n"
            )

        prompt = f"""
Summarize the following conversation.

Keep the summary concise.

Focus on:

- user goals

- important facts

- previous decisions

Conversation:

{conversation}

Summary:
"""

        return generate_answer(prompt)