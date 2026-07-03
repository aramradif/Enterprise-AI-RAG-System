from app.core.context_manager import select_context
from app.llm.prompt_builder import build_prompt
from app.llm.rag import generate_answer, stream_answer
from app.memory.conversation_manager import ConversationManager
from app.retrieval.hybrid_search import hybrid_search


class RAGService:
    """
    Enterprise RAG Service.

    Coordinates:
    - Hybrid Retrieval
    - Context Management
    - Conversation Memory
    - Prompt Building
    - GPT Answer Generation
    """

    def __init__(self):
        self.conversation = ConversationManager()

    def retrieve(
        self,
        query: str,
    ):
        """
        Retrieve relevant documents using hybrid search.
        """
        return hybrid_search(query)

    def build_prompt(
        self,
        question: str,
    ):
        """
        Build an enterprise prompt containing:

        - Conversation summary
        - Recent conversation history
        - Retrieved documents
        - User question
        """

        context = self.retrieve(question)

        context = select_context(
            context,
            max_documents=3,
        )

        return build_prompt(
            question=question,
            context=context,
            history=self.conversation.get_history(),
            summary=self.conversation.get_summary(),
        )

    def answer(
        self,
        question: str,
    ):
        """
        Standard (non-streaming) RAG pipeline.
        """

        self.conversation.add_user_message(
            question,
        )

        prompt = self.build_prompt(question)

        answer = generate_answer(prompt)

        self.conversation.add_assistant_message(
            answer,
        )

        return answer

    def stream(
        self,
        question: str,
    ):
        """
        Streaming Enterprise RAG pipeline.

        Returns GPT response incrementally.
        """

        self.conversation.add_user_message(
            question,
        )

        prompt = self.build_prompt(question)

        return stream_answer(prompt)