from app.retrieval.hybrid_search import hybrid_search
from app.llm.prompt_builder import build_prompt
from app.llm.rag import generate_answer
from app.core.context_manager import select_context


class RAGService:
    """
    Enterprise RAG Service.

    Coordinates retrieval and prompt creation.
    """

    def retrieve(
        self,
        query: str,
    ):
        return hybrid_search(query)

    def build_prompt(
        self,
        question: str,
    ):
        context = self.retrieve(question)

        context = select_context(
            context,
            max_documents=3,
        )

        prompt = build_prompt(
            question=question,
            context=context,
        )

        return prompt

    def answer(
        self,
        question: str,
    ):
        """
        Complete Enterprise RAG pipeline.
        """

        prompt = self.build_prompt(question)

        return generate_answer(prompt)