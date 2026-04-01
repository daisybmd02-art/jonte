from sqlalchemy.orm import Session
from app.db.models import Leader


def seed_leaders(db: Session):
    # Prevent duplicate seeding
    if db.query(Leader).count() > 0:
        return

    leaders = [
        Leader(
            name="Governor Example",
            role="Governor",
            county="Kiambu",
            party="Independent",
            bio="Leads the county executive and oversees service delivery."
        ),
        Leader(
            name="Senator Example",
            role="Senator",
            county="Kiambu",
            party="Example Party",
            bio="Represents county interests in the Senate."
        ),
        Leader(
            name="MP Example",
            role="MP",
            county="Kiambu",
            constituency="Thika Town",
            party="Example Party",
            bio="Represents the constituency in the National Assembly."
        ),
        Leader(
            name="MCA Example",
            role="MCA",
            county="Kiambu",
            constituency="Thika Town",
            party="Example Party",
            bio="Represents ward residents in the County Assembly."
        ),
    ]

    db.add_all(leaders)
    db.commit()
