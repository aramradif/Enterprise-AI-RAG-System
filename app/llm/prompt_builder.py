from app.models.chat import ChatMessage


def build_prompt(
    question: str,
    context: list,
    history: list[ChatMessage] | None = None,
    summary: str = "",
):
    """
    Build an enterprise RAG prompt.

    The prompt distinguishes between:
    - conversation-focused questions;
    - document-focused knowledge questions.

    It prioritizes conversation memory when the user asks
    about the current discussion, while preserving grounded
    RAG behavior for questions that require retrieved documents.
    """

    conversation_lines = []

    if history:
        for message in history:
            role_label = (
                "User"
                if message.role == "user"
                else "Assistant"
            )

            conversation_lines.append(
                f"{role_label}: {message.content}"
            )

    conversation = "\n".join(conversation_lines)

    retrieved_documents = []

    for index, document in enumerate(
        context,
        start=1,
    ):
        if isinstance(document, dict):
            content = document.get(
                "content",
                "",
            )

            source = document.get(
                "source",
                "Unknown source",
            )

            retrieved_documents.append(
                (
                    f"[Document {index}]\n"
                    f"Source: {source}\n"
                    f"Content: {content}"
                )
            )

        else:
            retrieved_documents.append(
                (
                    f"[Document {index}]\n"
                    f"Content: {str(document)}"
                )
            )

    retrieved_context = "\n\n".join(
        retrieved_documents
    )

    prompt = f"""
You are an enterprise educational AI assistant.

Your job is to answer the current user question using the most
relevant information available from:

1. The current conversation summary
2. The recent conversation history
3. The retrieved documents

Follow these rules carefully:

- If the user asks about the conversation itself, such as:
  "What did we discuss?",
  "Summarize our conversation.",
  "What was my previous question?",
  "What did I ask earlier?",
  "Continue where we left off.",
  then prioritize the conversation summary and recent conversation.

- For conversation-focused questions, do not summarize the retrieved
  documents unless the user specifically asks about them.

- If the user asks a knowledge question about course content,
  policies, documents, definitions, or other external information,
  use the retrieved documents as the primary source.

- Use conversation history to understand follow-up questions,
  references, pronouns, and user intent.

- Do not invent facts that are not supported by either the
  conversation or the retrieved documents.

- If the answer cannot be found in the conversation or retrieved
  documents, clearly say that the available information is
  insufficient.

- Keep the answer direct, clear, and useful.

Conversation Summary:
---------------------
{summary or "No conversation summary is available."}

Recent Conversation:
--------------------
{conversation or "No recent conversation history is available."}

Retrieved Documents:
-------------------
{retrieved_context or "No retrieved documents are available."}

Current User Question:
---------------------
{question}

Answer:
"""

    return prompt.strip()