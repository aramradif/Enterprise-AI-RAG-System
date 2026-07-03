from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.ask import router as ask_router

app = FastAPI(
    title="RAG Learning Assistant API",
    description="Production-ready Retrieval-Augmented Generation API",
    version="1.0.0",
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
