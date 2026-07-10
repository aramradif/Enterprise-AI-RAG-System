import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LOG_FILE = Path("data/logs/rag_requests.json")


def ensure_log_file() -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not LOG_FILE.exists():
        LOG_FILE.write_text("[]", encoding="utf-8")


def write_log_entry(entry: dict[str, Any]) -> None:
    ensure_log_file()

    logs = json.loads(
        LOG_FILE.read_text(encoding="utf-8")
    )

    logs.append(entry)

    LOG_FILE.write_text(
        json.dumps(logs, indent=2),
        encoding="utf-8",
    )


def create_log_entry(
    question: str,
    metrics: dict[str, Any],
    status: str = "success",
) -> dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "status": status,
        "retrieval_time_ms": metrics["retrieval"]["retrieval_time_ms"],
        "llm_time_ms": metrics["generation"]["llm_time_ms"],
        "documents_retrieved": metrics["retrieval"]["documents_retrieved"],
        "prompt_tokens": metrics["generation"]["prompt_tokens"],
        "completion_tokens": metrics["generation"]["completion_tokens"],
        "total_tokens": metrics["generation"]["total_tokens"],
        "estimated_cost_usd": metrics["cost"]["estimated_cost_usd"],
    }