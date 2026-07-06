from app.evaluation.evaluator import create_metrics, update_token_metrics
from app.evaluation.report import build_evaluation_report


metrics = create_metrics("What is RAG?")

metrics.retrieval_time_ms = 42.5
metrics.llm_time_ms = 1840.2
metrics.documents_retrieved = 5
metrics.context_length_chars = 2184
metrics.prompt_length_chars = 3101

metrics = update_token_metrics(
    metrics=metrics,
    prompt_tokens=534,
    completion_tokens=182,
)

report = build_evaluation_report(metrics)

print(report)