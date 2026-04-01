from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import UserProfile, User
from app.schemas.profile import ProfileBase, ProfileOut
from app.core.deps import get_current_user
router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=ProfileOut)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not set yet")
    return profile


@router.put("", response_model=ProfileOut)
def upsert_profile(
    payload: ProfileBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id).first()
    data = payload.model_dump()

    if not profile:
        profile = UserProfile(user_id=current_user.id,
                              **data)  # ✅ sets user_id
        db.add(profile)
    else:
        for k, v in data.items():
            setattr(profile, k, v)

    db.commit()
    db.refresh(profile)
    return profile
