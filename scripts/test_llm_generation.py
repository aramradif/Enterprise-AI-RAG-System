from app.llm.rag import generate_answer

answer = generate_answer(
    "Explain Retrieval-Augmented Generation in one sentence."
)

print(answer)