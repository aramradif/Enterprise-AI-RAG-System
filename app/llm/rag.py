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
        temperature=0,
    )

    return response.choices[0].message.content