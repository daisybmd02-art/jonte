import json
import os
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Leader

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "knowledge",
    "leaders_real.json"
)


def load_real_leaders():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def upsert_real_leader(db: Session, payload: dict):
    existing = db.query(Leader).filter(
        Leader.role == payload.get("role"),
        Leader.county == payload.get("county"),
        Leader.constituency == payload.get("constituency"),
        Leader.ward == payload.get("ward"),
    ).first()

    if existing:
        existing.name = payload.get("name")
        existing.party = payload.get("party")
        existing.level = payload.get("level")
        existing.bio = payload.get("bio")
        existing.work_summary = payload.get("work_summary")
        existing.achievements = payload.get("achievements")
        existing.image_path = payload.get("image_path")
        existing.photo_url = payload.get("photo_url")
    else:
        db.add(Leader(**payload))


def main():
    db = SessionLocal()
    rows = load_real_leaders()

    for payload in rows:
        upsert_real_leader(db, payload)

    db.commit()
    db.close()
    print("✅ Imported real leaders")


if __name__ == "__main__":
    main()
