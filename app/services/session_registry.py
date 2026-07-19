from app.memory.session_manager import SessionManager
from app.services.session_service import SessionService


session_manager = SessionManager(
    max_history=6,
)

session_service = SessionService(
    session_manager=session_manager,
)