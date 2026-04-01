from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.leader import Leader  # noqa: F401
from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base

router = APIRouter(prefix="/leaders", tags=["leaders"])


class Leader(Base):
    __tablename__ = "leaders"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(120), nullable=False, index=True)
    # President, Governor, MP, MCA, Senator...
    role = Column(String(80), nullable=False, index=True)
    party = Column(String(80), nullable=True)

    # Where they represent
    # NATIONAL | COUNTY | CONSTITUENCY | WARD
    level = Column(String(20), nullable=False, index=True)
    county = Column(String(80), nullable=True, index=True)
    constituency = Column(String(80), nullable=True, index=True)
    ward = Column(String(80), nullable=True, index=True)

    photo_url = Column(Text, nullable=True)
    work_summary = Column(Text, nullable=True)
    achievements = Column(Text, nullable=True)


@router.get("/")
def list_leaders(db: Session = Depends(get_db)):
    return db.query(Leader).all()


@router.get("/by-location")
def leaders_by_location(
    county: str,
    constituency: str = None,
    ward: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Leader).filter(Leader.county == county)

    if constituency:
        query = query.filter(Leader.constituency == constituency)

    if ward:
        query = query.filter(Leader.ward == ward)

    return query.all()
