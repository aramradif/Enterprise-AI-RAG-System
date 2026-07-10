from app.core.context_manager import select_context
from app.evaluation.evaluator import (
    create_metrics,
    current_time,
    elapsed_ms,
    update_token_metrics,
)
from app.evaluation.report import build_evaluation_report
from app.llm.prompt_builder import build_prompt
from app.llm.rag import generate_answer, stream_answer
from app.logging.logger import (
    create_log_entry,
    write_log_entry,
)
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
    - Evaluation Metrics
    - Observability Logging
    """

    def __init__(self):
        self.conversation = ConversationManager()

    def retrieve(self, query: str):
        """
        Retrieve relevant documents using hybrid search.
        """
        return hybrid_search(query)

    def build_prompt(self, question: str):
        """
        Build an enterprise prompt.
        """

        context = self.retrieve(question)

        context = select_context(
            context,
            max_documents=3,
        )

        prompt = build_prompt(
            question=question,
            context=context,
            history=self.conversation.get_history(),
            summary=self.conversation.get_summary(),
        )

        return prompt, context

    def answer(self, question: str):
        """
        Standard RAG pipeline.
        Returns only the answer string.
        """

        self.conversation.add_user_message(question)

        prompt, context = self.build_prompt(question)

        llm_result = generate_answer(prompt)

        self.conversation.add_assistant_message(llm_result.answer)

        return llm_result.answer

    def answer_with_metrics(self, question: str):
        """
        RAG pipeline with enterprise evaluation metrics
        and observability logging.
        """

        metrics = create_metrics(question)

        self.conversation.add_user_message(question)

        retrieval_start = current_time()

        raw_context = self.retrieve(question)

        context = select_context(
            raw_context,
            max_documents=3,
        )

        metrics.retrieval_time_ms = elapsed_ms(retrieval_start)
        metrics.documents_retrieved = len(context)
        metrics.context_length_chars = sum(
            len(document.get("content", ""))
            for document in context
        )

        prompt = build_prompt(
            question=question,
            context=context,
            history=self.conversation.get_history(),
            summary=self.conversation.get_summary(),
        )

        metrics.prompt_length_chars = len(prompt)

        llm_start = current_time()

        llm_result = generate_answer(prompt)

        metrics.llm_time_ms = elapsed_ms(llm_start)

        metrics = update_token_metrics(
            metrics=metrics,
            prompt_tokens=llm_result.prompt_tokens,
            completion_tokens=llm_result.completion_tokens,
        )

        self.conversation.add_assistant_message(llm_result.answer)

        evaluation_report = build_evaluation_report(metrics)

        log_entry = create_log_entry(
            question=question,
            metrics=evaluation_report,
            status="success",
        )

        write_log_entry(log_entry)

        return {
            "answer": llm_result.answer,
            "metrics": evaluation_report,
        }

    def stream(self, question: str):
        """
        Streaming Enterprise RAG pipeline.
        """

        self.conversation.add_user_message(question)

        prompt, context = self.build_prompt(question)

        return stream_answer(prompt)