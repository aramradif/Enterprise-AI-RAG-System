from app.llm.rag import stream_answer


prompt = """
Explain Retrieval-Augmented Generation.
"""

print()

print("Streaming Response")

print("------------------")

for token in stream_answer(prompt):

    print(
        token,
        end="",
        flush=True,
    )

print()