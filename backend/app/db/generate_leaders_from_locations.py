import json
import os
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Leader

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "knowledge",
    "kenya_locations.json"
)


def load_locations():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def upsert_placeholder(db: Session, payload: dict):
    """
    Insert placeholder leader only if missing.
    Do not overwrite real data that may already exist.
    Unique key = role + county + constituency + ward
    """
    existing = db.query(Leader).filter(
        Leader.role == payload.get("role"),
        Leader.county == payload.get("county"),
        Leader.constituency == payload.get("constituency"),
        Leader.ward == payload.get("ward"),
    ).first()

    if existing:
        return

    db.add(Leader(**payload))


def main():
    locations = load_locations()
    db = SessionLocal()

    # National placeholders
    upsert_placeholder(db, {
        "name": "President (Set Real Name Later)",
        "role": "President",
        "level": "NATIONAL",
        "party": None,
        "county": None,
        "constituency": None,
        "ward": None,
        "bio": "National leader (placeholder).",
        "work_summary": "National leadership and public policy.",
        "photo_url": None,
        "image_path": "/images/leaders/default-leader.jpg",
    })

    upsert_placeholder(db, {
        "name": "Deputy President (Set Real Name Later)",
        "role": "Deputy President",
        "level": "NATIONAL",
        "party": None,
        "county": None,
        "constituency": None,
        "ward": None,
        "bio": "National leader (placeholder).",
        "work_summary": "Supports national leadership and coordination.",
        "photo_url": None,
        "image_path": "/images/leaders/default-leader.jpg",
    })

    # County / constituency / ward placeholders
    for county, consts in locations.items():
        upsert_placeholder(db, {
            "name": f"Governor of {county} (Set Real Name Later)",
            "role": "Governor",
            "level": "COUNTY",
            "party": None,
            "county": county,
            "constituency": None,
            "ward": None,
            "bio": f"Governor for {county} (placeholder).",
            "work_summary": "County leadership, services, and development.",
            "photo_url": None,
            "image_path": "/images/leaders/default-leader.jpg",
        })

        upsert_placeholder(db, {
            "name": f"Senator of {county} (Set Real Name Later)",
            "role": "Senator",
            "level": "COUNTY",
            "party": None,
            "county": county,
            "constituency": None,
            "ward": None,
            "bio": f"Senator for {county} (placeholder).",
            "work_summary": "County oversight and devolution.",
            "photo_url": None,
            "image_path": "/images/leaders/default-leader.jpg",
        })

        for constituency, wards in consts.items():
            upsert_placeholder(db, {
                "name": f"MP for {constituency} (Set Real Name Later)",
                "role": "MP",
                "level": "CONSTITUENCY",
                "party": None,
                "county": county,
                "constituency": constituency,
                "ward": None,
                "bio": f"MP for {constituency} in {county} (placeholder).",
                "work_summary": "Constituency representation and national legislation.",
                "photo_url": None,
                "image_path": "/images/leaders/default-leader.jpg",
            })

            for ward in wards:
                upsert_placeholder(db, {
                    "name": f"MCA for {ward} (Set Real Name Later)",
                    "role": "MCA",
                    "level": "WARD",
                    "party": None,
                    "county": county,
                    "constituency": constituency,
                    "ward": ward,
                    "bio": f"MCA for {ward} ward (placeholder).",
                    "work_summary": "Ward representation and county oversight.",
                    "photo_url": None,
                    "image_path": "/images/leaders/default-leader.jpg",
                })

    db.commit()
    db.close()
    print("✅ Generated leaders for all locations")


if __name__ == "__main__":
    main()
