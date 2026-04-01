from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Leader
from sqlalchemy import or_

router = APIRouter(prefix="/leaders", tags=["leaders"])


@router.get("")
def list_leaders(
    level: str | None = Query(default=None),
    county: str | None = Query(default=None),
    constituency: str | None = Query(default=None),
    ward: str | None = Query(default=None),
    q: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Leader)

    if level:
        query = query.filter(Leader.level == level)
    if county:
        query = query.filter(Leader.county.ilike(f"%{county}%"))
    if constituency:
        query = query.filter(Leader.constituency.ilike(f"%{constituency}%"))
    if ward:
        query = query.filter(Leader.ward.ilike(f"%{ward}%"))
    if q:
        query = query.filter(Leader.name.ilike(f"%{q}%"))

    return query.order_by(Leader.level.asc(), Leader.role.asc()).limit(500).all()


@router.get("/public")
def public_leaders(db: Session = Depends(get_db)):
    # Everyone can see national leaders
    return (
        db.query(Leader)
        .filter(Leader.level == "NATIONAL")
        .order_by(Leader.role.asc())
        .all()
    )


@router.get("/by-location")
def leaders_by_location(
    county: str,
    constituency: str | None = None,
    ward: str | None = None,
    db: Session = Depends(get_db),
):
    # Return a bundle: county + constituency + ward leaders (not overly strict)
    county_norm = county.replace(" City", "").strip()
    q = db.query(Leader).filter(Leader.county.ilike(f"%{county_norm}%"))
    # If constituency provided, allow either constituency-level or county-level leaders
    if constituency:
        q = q.filter(or_(Leader.constituency == None,
                     Leader.constituency == constituency))

    # If ward provided, allow either ward-level or higher-level leaders
    if ward:
        q = q.filter(or_(Leader.ward == None, Leader.ward == ward))

    return q.order_by(Leader.level.asc(), Leader.role.asc()).all()


@router.get("/{leader_id}")
def get_leader(leader_id: int, db: Session = Depends(get_db)):
    row = db.query(Leader).filter(Leader.id == leader_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Leader not found")
    return row
