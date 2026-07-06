import time

from app.evaluation.metrics import RAGMetrics


GPT_4O_MINI_INPUT_COST_PER_1M = 0.15
GPT_4O_MINI_OUTPUT_COST_PER_1M = 0.60


def current_time() -> float:
    return time.perf_counter()


def elapsed_ms(start_time: float) -> float:
    return round((time.perf_counter() - start_time) * 1000, 2)


def estimate_gpt_4o_mini_cost(
    prompt_tokens: int,
    completion_tokens: int,
) -> float:
    input_cost = (prompt_tokens / 1_000_000) * GPT_4O_MINI_INPUT_COST_PER_1M
    output_cost = (completion_tokens / 1_000_000) * GPT_4O_MINI_OUTPUT_COST_PER_1M

    return round(input_cost + output_cost, 8)


def create_metrics(question: str) -> RAGMetrics:
    return RAGMetrics(question=question)


def update_token_metrics(
    metrics: RAGMetrics,
    prompt_tokens: int,
    completion_tokens: int,
) -> RAGMetrics:
    metrics.prompt_tokens = prompt_tokens
    metrics.completion_tokens = completion_tokens
    metrics.total_tokens = prompt_tokens + completion_tokens
    metrics.estimated_cost_usd = estimate_gpt_4o_mini_cost(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )

    return metrics