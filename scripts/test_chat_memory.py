from app.services.rag_service import RAGService

service = RAGService()

print("\n========== Question 1 ==========\n")

answer1 = service.answer(
    "What is Retrieval-Augmented Generation?"
)

print(answer1)

print("\n========== Question 2 ==========\n")

answer2 = service.answer(
    "Why is it useful?"
)

print(answer2)

print("\n========== Conversation History ==========\n")

for message in service.conversation.get_history():
    print(f"{message.role}: {message.content[:100]}...")