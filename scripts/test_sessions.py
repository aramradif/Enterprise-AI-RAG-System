from app.memory.session_manager import SessionManager

sessions = SessionManager()

adam = sessions.get_conversation("adam")

john = sessions.get_conversation("john")

adam.add_user_message("What is RAG?")

john.add_user_message("What is FastAPI?")

print()

print("Adam")

for message in adam.get_history():
    print(message.content)

print()

print("John")

for message in john.get_history():
    print(message.content)