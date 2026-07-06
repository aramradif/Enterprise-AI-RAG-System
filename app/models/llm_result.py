from dataclasses import dataclass


@dataclass
class LLMResult:
    answer: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0