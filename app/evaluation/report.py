from app.evaluation.metrics import RAGMetrics


def build_evaluation_report(metrics: RAGMetrics) -> dict:
    return {
        "question": metrics.question,
        "retrieval": {
            "retrieval_time_ms": metrics.retrieval_time_ms,
            "documents_retrieved": metrics.documents_retrieved,
            "context_length_chars": metrics.context_length_chars,
        },
        "generation": {
            "llm_time_ms": metrics.llm_time_ms,
            "prompt_length_chars": metrics.prompt_length_chars,
            "prompt_tokens": metrics.prompt_tokens,
            "completion_tokens": metrics.completion_tokens,
            "total_tokens": metrics.total_tokens,
        },
        "cost": {
            "estimated_cost_usd": metrics.estimated_cost_usd,
        },
    }