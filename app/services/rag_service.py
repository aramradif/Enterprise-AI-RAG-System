from collections.abc import Generator

from app.core.citations import (
    attach_citations,
    build_citations,
    format_citations,
)
from app.core.context_manager import select_context
from app.core.query_router import is_conversation_question
from app.evaluation.evaluator import (
    create_metrics,
    current_time,
    elapsed_ms,
    update_token_metrics,
)
from app.evaluation.report import build_evaluation_report
from app.llm.conversation_prompt_builder import (
    build_conversation_prompt,
)
from app.llm.prompt_builder import build_prompt
from app.llm.rag import generate_answer, stream_answer
from app.logging.logger import (
    create_log_entry,
    write_log_entry,
)
from app.memory.conversation_manager import ConversationManager
from app.retrieval.hybrid_search import hybrid_search
from app.services.session_registry import session_manager


DEFAULT_SESSION_ID = "enterprise-demo"


class RAGService:
    """
    Enterprise RAG Service.

    Coordinates:
    - Query intent routing
    - Conversation-memory prompting
    - Hybrid document retrieval
    - Context management
    - Deterministic source citations
    - Session-based conversation memory
    - GPT answer generation
    - Streaming responses
    - Evaluation metrics
    - Observability logging
    """

    def retrieve(
        self,
        query: str,
    ):
        """
        Retrieve relevant documents using hybrid search.
        """

        return hybrid_search(query)

    def get_conversation(
        self,
        session_id: str = DEFAULT_SESSION_ID,
    ) -> ConversationManager:
        """
        Return the ConversationManager associated
        with the selected session.
        """

        return session_manager.get_conversation(
            session_id=session_id,
        )

    def prepare_context(
        self,
        question: str,
    ) -> tuple[list, bool]:
        """
        Route the question to conversation memory
        or document retrieval.

        Returns:
            context:
                Selected retrieved documents, or an
                empty list for conversation questions.

            conversation_question:
                True when retrieval should be skipped.
        """

        conversation_question = is_conversation_question(
            question,
        )

        if conversation_question:
            return [], True

        raw_context = self.retrieve(
            question,
        )

        selected_context = select_context(
            raw_context,
            max_documents=3,
        )

        return selected_context, False

    def create_prompt(
        self,
        question: str,
        conversation: ConversationManager,
        context: list,
        conversation_question: bool,
    ) -> str:
        """
        Build the appropriate prompt for the routed question.

        Conversation questions use session memory only.
        Knowledge questions use the document-grounded RAG prompt.
        """

        history = conversation.get_history()
        summary = conversation.get_summary()

        if conversation_question:
            return build_conversation_prompt(
                question=question,
                history=history,
                summary=summary,
            )

        return build_prompt(
            question=question,
            context=context,
            history=history,
            summary=summary,
        )

    @staticmethod
    def add_answer_citations(
        answer: str,
        context: list,
        conversation_question: bool,
    ) -> tuple[str, list[dict]]:
        """
        Attach deterministic citations to document-grounded answers.

        Conversation-memory answers do not receive document citations
        because document retrieval was intentionally skipped.
        """

        if conversation_question:
            return answer.strip(), []

        cited_answer, citations = attach_citations(
            answer=answer,
            context=context,
        )

        return cited_answer, citations

    def build_prompt(
        self,
        question: str,
        session_id: str = DEFAULT_SESSION_ID,
    ):
        """
        Route the question and construct the appropriate prompt.

        The prompt is built before the current user message is saved,
        so conversation-focused questions only inspect earlier history.
        """

        conversation = self.get_conversation(
            session_id=session_id,
        )

        context, conversation_question = (
            self.prepare_context(
                question,
            )
        )

        prompt = self.create_prompt(
            question=question,
            conversation=conversation,
            context=context,
            conversation_question=conversation_question,
        )

        return (
            prompt,
            context,
            conversation_question,
        )

    def answer(
        self,
        question: str,
        session_id: str = DEFAULT_SESSION_ID,
    ) -> str:
        """
        Standard non-streaming answer pipeline.

        Document-grounded answers receive deterministic citations.
        Conversation-memory answers do not receive document citations.
        """

        conversation = self.get_conversation(
            session_id=session_id,
        )

        (
            prompt,
            context,
            conversation_question,
        ) = self.build_prompt(
            question=question,
            session_id=session_id,
        )

        conversation.add_user_message(
            question,
        )

        llm_result = generate_answer(
            prompt,
        )

        cited_answer, _ = self.add_answer_citations(
            answer=llm_result.answer,
            context=context,
            conversation_question=conversation_question,
        )

        conversation.add_assistant_message(
            cited_answer,
        )

        session_manager.touch_session(
            session_id,
        )

        return cited_answer

    def answer_with_metrics(
        self,
        question: str,
        session_id: str = DEFAULT_SESSION_ID,
    ):
        """
        Evaluation pipeline with intelligent routing,
        deterministic citations, metrics, and logging.

        Conversation questions intentionally report:
        - zero retrieved documents;
        - zero retrieved-context characters;
        - no citations;
        - retrieval_skipped as True.
        """

        conversation = self.get_conversation(
            session_id=session_id,
        )

        metrics = create_metrics(
            question,
        )

        retrieval_start = current_time()

        context, conversation_question = (
            self.prepare_context(
                question,
            )
        )

        metrics.retrieval_time_ms = elapsed_ms(
            retrieval_start,
        )

        metrics.documents_retrieved = len(
            context,
        )

        metrics.context_length_chars = sum(
            (
                len(document.get("content", ""))
                if isinstance(document, dict)
                else len(str(document))
            )
            for document in context
        )

        prompt = self.create_prompt(
            question=question,
            conversation=conversation,
            context=context,
            conversation_question=conversation_question,
        )

        metrics.prompt_length_chars = len(
            prompt,
        )

        conversation.add_user_message(
            question,
        )

        llm_start = current_time()

        llm_result = generate_answer(
            prompt,
        )

        metrics.llm_time_ms = elapsed_ms(
            llm_start,
        )

        metrics = update_token_metrics(
            metrics=metrics,
            prompt_tokens=llm_result.prompt_tokens,
            completion_tokens=llm_result.completion_tokens,
        )

        cited_answer, citations = (
            self.add_answer_citations(
                answer=llm_result.answer,
                context=context,
                conversation_question=conversation_question,
            )
        )

        conversation.add_assistant_message(
            cited_answer,
        )

        session_manager.touch_session(
            session_id,
        )

        evaluation_report = build_evaluation_report(
            metrics,
        )

        evaluation_report["routing"] = {
            "conversation_question": conversation_question,
            "retrieval_skipped": conversation_question,
            "prompt_type": (
                "conversation_memory"
                if conversation_question
                else "document_rag"
            ),
        }

        evaluation_report["citations"] = citations

        log_entry = create_log_entry(
            question=question,
            metrics=evaluation_report,
            status="success",
        )

        write_log_entry(
            log_entry,
        )

        return {
            "answer": cited_answer,
            "citations": citations,
            "metrics": evaluation_report,
        }

    def stream(
        self,
        question: str,
        session_id: str = DEFAULT_SESSION_ID,
    ) -> Generator[str, None, None]:
        """
        Streaming pipeline with intelligent routing and citations.

        Document citations are streamed after the model finishes.
        The complete displayed answer is then stored in the selected
        conversation session.
        """

        conversation = self.get_conversation(
            session_id=session_id,
        )

        (
            prompt,
            context,
            conversation_question,
        ) = self.build_prompt(
            question=question,
            session_id=session_id,
        )

        conversation.add_user_message(
            question,
        )

        def response_generator() -> Generator[str, None, None]:
            answer_chunks: list[str] = []

            try:
                for chunk in stream_answer(
                    prompt,
                ):
                    answer_chunks.append(
                        chunk,
                    )

                    yield chunk

                if not conversation_question:
                    citations = build_citations(
                        context,
                    )

                    citation_text = format_citations(
                        citations,
                    )

                    if citation_text:
                        yield citation_text

            finally:
                generated_answer = "".join(
                    answer_chunks,
                ).strip()

                cited_answer, _ = (
                    self.add_answer_citations(
                        answer=generated_answer,
                        context=context,
                        conversation_question=conversation_question,
                    )
                )

                if cited_answer:
                    conversation.add_assistant_message(
                        cited_answer,
                    )

                session_manager.touch_session(
                    session_id,
                )

        return response_generator()