from app.config.settings import settings
from app.llm.openai_client import client


def generate_answer(
    prompt: str,
) -> str:
    """
    Generate an answer using GPT.
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

    return response.choices[0].message.content


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

            # Print every streamed chunk to the terminal
            # This helps verify whether OpenAI is sending
            # true incremental chunks or buffering them.
            print(repr(delta))

            yield delta