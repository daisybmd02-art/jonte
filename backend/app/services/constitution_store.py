import os
import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import pdfplumber


PDF_PATH = os.path.join(os.path.dirname(__file__), "..",
                        "knowledge", "constitution.pdf")


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


@dataclass
class Chunk:
    page: int
    text: str


class ConstitutionStore:
    def __init__(self, chunks: List[Chunk]):
        self.chunks = chunks

    def get_chunk(self, chunk_id: int) -> Optional[Chunk]:
        # since you used page number as id
        for ch in self.chunks:
            if ch.page == chunk_id:
                return ch
        return None

    def search(self, query: str, top_k: int = 6) -> List[Dict[str, Any]]:
        q = (query or "").lower().strip()
        if not q:
            return []

        scored = []
        for idx, ch in enumerate(self.chunks):
            t = ch.text.lower()
            score = t.count(q)
            for tok in q.split():
                if len(tok) >= 4:
                    score += t.count(tok)
            if score > 0:
                scored.append((score, idx, ch))

        scored.sort(key=lambda x: x[0], reverse=True)

        out = []
        for score, idx, ch in scored[:top_k]:
            excerpt = ch.text[:260] + ("..." if len(ch.text) > 260 else "")
            out.append({
                "id": idx,       # ✅ real stable id
                "page": ch.page,
                "excerpt": excerpt,
                "score": score
            })
        return out


_STORE = None


def get_constitution_store() -> ConstitutionStore:
    global _STORE
    if _STORE is not None:
        return _STORE

    abs_path = os.path.abspath(PDF_PATH)
    print("PDF_PATH absolute =", abs_path, flush=True)
    print("PDF exists? =", os.path.exists(PDF_PATH), flush=True)

    if not os.path.exists(PDF_PATH):
        raise RuntimeError(f"constitution.pdf not found at: {abs_path}")

    chunks: List[Chunk] = []
    with pdfplumber.open(PDF_PATH) as pdf:
        for i, page in enumerate(pdf.pages):
            txt = _clean(page.extract_text() or "")
            if txt:
                chunks.append(Chunk(page=i + 1, text=txt))

    _STORE = ConstitutionStore(chunks)
    print(
        f"✅ Loaded Constitution store: {len(chunks)} pages/chunks", flush=True)
    return _STORE


def load_constitution_store() -> List[Dict[str, Any]]:
    """
    Compatibility wrapper for RAG.
    Returns: [{"page": int, "text": str, "source": "constitution"}, ...]
    """
    store = get_constitution_store()
    return [{"page": ch.page, "text": ch.text, "source": "constitution"} for ch in store.chunks]
