from app.memory.conversation_manager import ConversationManager

conversation = ConversationManager(
    max_history=6,
)

# Simulate a long conversation
for i in range(12):
    conversation.add_user_message(
        f"Question {i}"
    )

print("\n========== Conversation Summary ==========\n")

print(
    conversation.get_summary()
)

print("\n========== Conversation Window ==========\n")

for message in conversation.get_history():
    print(message.content)