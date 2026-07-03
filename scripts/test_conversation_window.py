from app.memory.conversation_manager import ConversationManager

conversation = ConversationManager(
    max_history=4,
)

for i in range(10):

    conversation.add_user_message(
        f"Question {i}"
    )

history = conversation.get_history()

print()

print("Conversation Window")

print("-------------------")

for message in history:

    print(message.content)