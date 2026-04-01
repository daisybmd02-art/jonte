from fastapi import APIRouter

from app.services.rag import rag
from app.services.constitution_store import load_constitution_store

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/reload-rag")
def reload_rag():
    chunks = load_constitution_store()
    rag.set_store(chunks)
    return {"ok": True, "chunks": len(chunks)}
