import json
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
)

LOG_FILE = Path("data/logs/rag_requests.json")


@router.get("")
def get_logs():
    """
    Return all Enterprise AI request logs.
    """

    if not LOG_FILE.exists():
        return []

    with open(
        LOG_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)