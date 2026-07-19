from app.models.chat import ChatMessage


def build_conversation_prompt(
    question: str,
    history: list[ChatMessage] | None = None,
    summary: str = "",
) -> str:
    """
    Build a prompt for conversation-memory questions.

    This prompt is used when the user asks about the current
    conversation, previous questions, prior answers, or requests
    a recap of the discussion.

    It intentionally excludes retrieved documents.
    """

    conversation_lines: list[str] = []

    if history:
        for index, message in enumerate(
            history,
            start=1,
        ):
            role_label = (
                "User"
                if message.role == "user"
                else "Assistant"
            )

            conversation_lines.append(
                (
                    f"Message {index}\n"
                    f"{role_label}: {message.content}"
                )
            )

    conversation_history = "\n\n".join(
        conversation_lines
    )

    prompt = f"""
You are an enterprise conversational AI assistant.

Answer the user's question using only the conversation summary
and recent conversation history provided below.

Follow these rules carefully:

- Focus on the conversation itself.
- Do not use or mention external documents.
- Do not introduce unrelated topics.
- When asked to summarize the discussion, summarize the entire
  available conversation in chronological order.
- Include brief but meaningful details from each major exchange.
- Do not repeat the current user's question as part of the
  earlier conversation unless it refers to a previous message.
- When asked what the user previously asked, identify the actual
  earlier user question or questions.
- When asked what the assistant previously said, identify the
  relevant prior assistant response.
- If the requested information is not present in the conversation,
  clearly say that it is not available.
- Keep the answer natural, direct, and concise.

Conversation Summary:
---------------------
{summary or "No earlier conversation summary is available."}

Recent Conversation History:
----------------------------
{
    conversation_history
    or "No recent conversation history is available."
}

Current User Question:
---------------------
{question}

Answer:
"""

    return prompt.strip()