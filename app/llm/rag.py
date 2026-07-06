from app.config.settings import settings
from app.llm.openai_client import client
from app.models.llm_result import LLMResult


def generate_answer(
    prompt: str,
) -> LLMResult:
    """
    Generate an answer using GPT and return
    both the answer and token usage.
    """

    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return LLMResult(
        answer=response.choices[0].message.content,
        prompt_tokens=response.usage.prompt_tokens,
        completion_tokens=response.usage.completion_tokens,
        total_tokens=response.usage.total_tokens,
    )


def stream_answer(
    prompt: str,
):
    """
    Stream an answer from GPT chunk by chunk.
    """

    stream = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        stream=True,
    )

    for chunk in stream:

        delta = chunk.choices[0].delta.content

        if delta:
            yield delta