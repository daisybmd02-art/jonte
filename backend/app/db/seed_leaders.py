from sqlalchemy.orm import Session
from app.db.models import Leader


def seed_leaders(db: Session):
    # Prevent duplicate seeding
    if db.query(Leader).count() > 0:
        return

    leaders = [
        # ---------- NATIONAL ----------
        Leader(
            name="William Ruto",
            role="President",
            party="UDA",
            level="NATIONAL",
            county=None,
            constituency=None,
            ward=None,
            bio="President of the Republic of Kenya.",
            photo_url=None,
        ),
        Leader(
            name="Rigathi Gachagua",
            role="Deputy President",
            party="UDA",
            level="NATIONAL",
            county=None,
            constituency=None,
            ward=None,
            bio="Deputy President of Kenya.",
            photo_url=None,
        ),

        # ---------- NAIROBI COUNTY ----------
        Leader(
            name="Johnson Sakaja",
            role="Governor",
            party="UDA",
            level="COUNTY",
            county="Nairobi",
            constituency=None,
            ward=None,
            bio="Governor of Nairobi City County.",
            photo_url=None,
        ),
        Leader(
            name="Edwin Sifuna",
            role="Senator",
            party="ODM",
            level="COUNTY",
            county="Nairobi",
            constituency=None,
            ward=None,
            bio="Senator representing Nairobi County.",
            photo_url=None,
        ),

        # ---------- DAGORETTI ----------
        Leader(
            name="MP Example Dagoretti",
            role="MP",
            party="Example Party",
            level="CONSTITUENCY",
            county="Nairobi",
            constituency="Dagoretti",
            ward=None,
            bio="Member of Parliament representing Dagoretti.",
            photo_url=None,
        ),

        # ---------- RIRUTA / RIRUTA WARD ----------
        Leader(
            name="MCA Example Riruta",
            role="MCA",
            party="Example Party",
            level="WARD",
            county="Nairobi",
            constituency="Dagoretti",
            ward="Riruta",
            bio="Member of County Assembly representing Riruta Ward.",
            photo_url=None,
        ),
    ]

    db.add_all(leaders)
    db.commit()
