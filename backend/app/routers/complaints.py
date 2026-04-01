from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Complaint
from app.schemas_root import ComplaintCreate, ComplaintOut, ComplaintStatusUpdate
from app.core.config import settings
from app.core.deps import get_current_user
from app.db.models import User, UserProfile


router = APIRouter(prefix="/complaints", tags=["complaints"])


def require_profile_location(db: Session, user_id: int) -> UserProfile:
    p = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not p or not p.county or not p.constituency or not p.ward:
        raise HTTPException(
            status_code=400, detail="Set your profile location before posting complaints")
    return p


def route_complaint(category: str):
    c = (category or "").lower()

    # County services
    if any(k in c for k in ["water", "sewer", "drain", "garbage", "waste", "roads", "road", "street", "lighting", "health", "hospital"]):
        return ("COUNTY", "County Service Department")

    # Ward/local admin issues
    if any(k in c for k in ["noise", "market", "blocking", "nuisance", "construction"]):
        return ("WARD", "Ward Administration")

    # National-level agencies (still keep location for filtering)
    if any(k in c for k in ["security", "police", "crime"]):
        return ("NATIONAL", "National Police Service")

    # Default
    return ("COUNTY", "General Service Desk")


@router.post("", response_model=ComplaintOut)
def create_complaint(payload: ComplaintCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    p = require_profile_location(db, user.id)

    data = payload.model_dump()

    # ✅ Always auto-fill from profile if missing
    data["county"] = data.get("county") or p.county
    data["constituency"] = data.get("constituency") or p.constituency
    data["ward"] = data.get("ward") or p.ward

    # ✅ Auto-routing (not to a person)
    routing_level, target_office = route_complaint(data.get("category"))
    data["routing_level"] = routing_level
    data["target_office"] = target_office

    c = Complaint(**data)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.get("", response_model=list[ComplaintOut])
def list_complaints(db: Session = Depends(get_db)):
    return db.query(Complaint).order_by(Complaint.created_at.desc()).limit(500).all()


@router.patch("/{complaint_id}/status", response_model=ComplaintOut)
def update_status(
    complaint_id: int,
    payload: ComplaintStatusUpdate,
    x_api_key: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if not x_api_key or x_api_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin key")

    row = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Complaint not found")

    row.status = payload.status
    db.commit()
    db.refresh(row)
    return row
