from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import settings
from app.database.session import engine
from app.storage.vector_storage import ChromaVectorStore

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    checks = {
        "postgres": "ok",
        "chroma": "ok",
    }

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        checks["postgres"] = "error"

    try:
        vector_store = ChromaVectorStore(
            persist_directory=settings.chroma_path,
            collection_name=settings.chroma_collection,
        )
        vector_store.count()
    except Exception:
        checks["chroma"] = "error"

    status = "ok" if all(value == "ok" for value in checks.values()) else "degraded"

    return {
        "status": status,
        "services": checks,
    }