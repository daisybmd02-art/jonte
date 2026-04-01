from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.services.rag import rag  # we will define rag below

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


class AskIn(BaseModel):
    question: str = Field(..., min_length=2)


class SourceOut(BaseModel):
    page: int
    excerpt: str


class AskOut(BaseModel):
    answer: str
    sources: List[SourceOut] = []
    meta: Optional[Dict[str, Any]] = None


@router.post("/", response_model=AskOut)
def ask_bot(payload: AskIn):
    q = payload.question.strip()

    result = rag.answer(q)  # ✅ returns dict

    answer = result.get("answer", "")
    sources = result.get("sources", [])

    # guarantee correct types for response_model
    if not isinstance(sources, list):
        sources = []

    if not answer or len(answer.strip()) < 10:
        answer = (
            "I found relevant Constitution passages for your question. "
            "Here is a simple summary based on the most relevant excerpts below."
        )

    return {"answer": answer, "sources": sources, "meta": {"mode": getattr(rag, "mode", "constitution")}}
