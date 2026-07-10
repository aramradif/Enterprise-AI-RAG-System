from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.ask import router as ask_router
from app.api.health import router as health_router
from app.api.logs import router as logs_router

app = FastAPI(
    title="Enterprise AI RAG System API",
    description=(
        "Production-ready Enterprise AI Retrieval-Augmented Generation (RAG) "
        "platform featuring hybrid retrieval, conversation memory, "
        "streaming responses, evaluation metrics, observability logging, "
        "and modular FastAPI architecture."
    ),
    version="1.8.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(ask_router)
app.include_router(logs_router)