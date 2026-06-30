from app.services.rag_service import RAGService

service = RAGService()

answer = service.answer(
    "What is Retrieval-Augmented Generation?"
)

print()
print("========== Enterprise RAG ==========")
print()
print(answer)