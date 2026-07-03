from app.services.rag_service import RAGService


service = RAGService()

print()

print("Streaming Enterprise RAG")

print("------------------------")

for chunk in service.stream(
    "What is Retrieval-Augmented Generation?"
):

    print(
        chunk,
        end="",
        flush=True,
    )

print()