from fastapi import APIRouter, Query, HTTPException
from app.services.constitution_store import get_constitution_store

router = APIRouter(prefix="/rights", tags=["rights"])


@router.get("/search")
def search_rights(q: str = Query(..., min_length=2)):
    print("RIGHTS HIT:", q, flush=True)
    try:
        store = get_constitution_store()
        print("STORE READY chunks:", len(store.chunks), flush=True)
        results = store.search(q, top_k=8)
        print("RESULTS:", len(results), flush=True)
        return {"count": len(results), "results": results}
    except Exception as e:
        print("RIGHTS ERROR:", repr(e), flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chunk/{chunk_id}")
def get_right_chunk(chunk_id: int):
    store = get_constitution_store()
    ch = store.get_chunk(chunk_id)
    if not ch:
        raise HTTPException(status_code=404, detail="Chunk not found")
    return {"id": chunk_id, "page": ch.page, "text": ch.text}


@router.get("/page/{page_num}")
def get_page(page_num: int):
    store = get_constitution_store()
    for ch in store.chunks:
        if ch.page == page_num:
            return {"page": ch.page, "text": ch.text}
    raise HTTPException(status_code=404, detail="Page not found")


@router.get("/health")
def rights_health():
    try:
        store = get_constitution_store()
        return {"ok": True, "chunks": len(store.chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
