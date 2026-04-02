from app.db.seed_leaders import seed_leaders
from app.db.session import SessionLocal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

from app.core.config import settings
from sqlalchemy import text

from app.routers import health, complaints, leaders, chatbot, admin, profile, rights

from app.services.rag import rag
from app.services.constitution_store import load_constitution_store
from app.routers import auth
from app.db.session import engine
from app.routers import locations
from app.db.base import Base  # or from app.db.models import Base
import traceback

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    seed_leaders(db)
finally:
    db.close()
app = FastAPI(title=settings.APP_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://jonteproject.netlify.app",

    ],

    # CORS (allow frontend)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(complaints.router)
app.include_router(leaders.router)
app.include_router(chatbot.router)
app.include_router(admin.router)
app.include_router(profile.router)
app.include_router(rights.router)
app.include_router(auth.router)
app.include_router(locations.router)

# @app.on_event("startup")
# def startup():
#    try:
#        chunks = load_constitution_store()
#        rag.set_store(chunks)
#        print(f"✅ Constitution AI ready: {len(chunks)} chunks loaded")
#   except Exception as e:
#       print("⚠️ Constitution AI failed (startup continues):", e)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/debug/tables")
def debug_tables():
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
        return {"tables": [r[0] for r in rows]}


@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        print("🔥 ERROR on", request.method, request.url)
        traceback.print_exc()
        raise
