from app.models.chat import ChatMessage


def build_prompt(
    question: str,
    context: list,
    history: list[ChatMessage] | None = None,
    summary: str = "",
):
    """
    Build an enterprise RAG prompt.

    Combines:
    - Conversation summary
    - Recent conversation history
    - Retrieved context
    - Current user question
    """

    conversation = ""

    if history:
        for message in history:
            conversation += (
                f"{message.role}: {message.content}\n"
            )

    retrieved_documents = []

    for doc in context:
        if isinstance(doc, dict):
            retrieved_documents.append(doc["content"])
        else:
            retrieved_documents.append(str(doc))

    retrieved_context = "\n\n".join(retrieved_documents)

    prompt = f"""
You are an educational AI assistant.

Use ONLY the retrieved context to answer the user's question.

If the conversation summary or recent conversation is useful,
use it to better understand the user's intent.

Conversation Summary:

{summary}

Recent Conversation:

{conversation}

Retrieved Context:

{retrieved_context}

Question:

{question}

Answer:
"""

    return prompt