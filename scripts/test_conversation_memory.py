from app.memory.conversation_memory import ConversationMemory

memory = ConversationMemory()

memory.add(
    role="user",
    content="What is RAG?",
)

memory.add(
    role="assistant",
    content="Retrieval-Augmented Generation combines retrieval with LLMs.",
)

print()

print("Conversation History")

print("--------------------")

for message in memory.get_messages():
    print(f"{message.role}: {message.content}")