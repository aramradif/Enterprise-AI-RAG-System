from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class RAGMetrics:
    question: str

    retrieval_time_ms: Optional[float] = None
    llm_time_ms: Optional[float] = None

    documents_retrieved: int = 0
    context_length_chars: int = 0
    prompt_length_chars: int = 0

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    estimated_cost_usd: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)