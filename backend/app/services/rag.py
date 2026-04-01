from typing import Any, Dict, List
import re
import math

from app.services.constitution_store import load_constitution_store


def _tokenize(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return [p for p in text.split() if len(p) > 2]


def _score(query_tokens: List[str], doc_tokens: List[str]) -> float:
    if not query_tokens or not doc_tokens:
        return 0.0
    qs = set(query_tokens)
    ds = set(doc_tokens)
    overlap = len(qs.intersection(ds))
    return overlap / math.sqrt(len(ds) + 1)


def _excerpt(text: str, max_len: int = 220) -> str:
    t = " ".join((text or "").split())
    if len(t) <= max_len:
        return t
    return t[: max_len - 1] + "…"


def _make_answer(question: str) -> str:
    """
    Light heuristic formatting. Keep this constitution-only to avoid circular imports.
    """
    q = question.lower()

    if "3 arms" in q or "three arms" in q or "arms of government" in q:
        return (
            "Kenya has three arms of government:\n"
            "1) Legislature (Parliament) — makes laws.\n"
            "2) Executive — implements laws and runs government.\n"
            "3) Judiciary — interprets laws and resolves disputes.\n"
            "See the citations below for supporting Constitution text."
        )

    if "complaint" in q or "report" in q or "issue" in q:
        return (
            "To submit a strong complaint:\n"
            "• Be specific: what happened, where (county/ward), and when.\n"
            "• Add evidence: photo/video, names, reference numbers.\n"
            "• State the impact and what remedy you want.\n"
            "Below are Constitution excerpts related to rights, oversight, and accountability."
        )

    if "freedom" in q or "rights" in q or "bill of rights" in q:
        return (
            "Rights and freedoms in Kenya are protected under the Bill of Rights.\n"
            "The citations below show relevant constitutional principles.\n"
            "If you tell me the exact right (speech, assembly, privacy, equality, arrest/detention), "
            "I can narrow to the most direct provisions."
        )

    if "who represents" in q or "leaders" in q or "mca" in q or "mp" in q or "governor" in q:
        return (
            "Representation usually includes: MCA (ward), MP (constituency), Senator (county), "
            "Woman Rep (county), and Governor (county executive).\n"
            "Below are Constitution excerpts touching on representation and governance structures."
        )

    return (
        "Here’s the most relevant guidance from the Constitution passages I have loaded.\n"
        "Check the citations below to verify the exact wording."
    )


class SimpleRAG:
    def __init__(self, store: List[Dict[str, Any]] | None = None):
        self.store: List[Dict[str, Any]] = store or []
        self.mode = "constitution"  # ✅ add this back

    # ✅ Compatibility methods (if your startup calls rag.load()/rag.build())
    def load(self):
        if not self.store:
            self.store = load_constitution_store()
        return self

    def build(self):
        # nothing to build in this simple engine
        return self

    def set_store(self, store: List[Dict[str, Any]]):
        self.store = store or []
        return self

    def ensure_loaded(self):
        if not self.store:
            self.store = load_constitution_store()

    def search(self, question: str, k: int = 5) -> List[Dict[str, Any]]:
        self.ensure_loaded()
        qt = _tokenize(question)

        scored: List[tuple[float, Dict[str, Any]]] = []
        for item in self.store:
            dt = _tokenize(item.get("text", "") or "")
            s = _score(qt, dt)
            if s > 0:
                scored.append((s, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [it for _, it in scored[:k]]

    def answer(self, question: str, k: int = 5) -> Dict[str, Any]:
        hits = self.search(question, k=k)

        sources = [
            {
                "page": int(h.get("page", 0) or 0),
                "excerpt": _excerpt(h.get("text", "")),
            }
            for h in hits
        ]

        return {
            "answer": _make_answer(question),
            "sources": sources,
        }


# ✅ Export a ready-to-use singleton
rag = SimpleRAG()
