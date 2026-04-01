from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.schemas.auth import SignupIn, LoginIn, TokenOut
from app.core.auth import hash_password, verify_password, create_access_token
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from app.core.auth import decode_token
from sqlalchemy.exc import IntegrityError
import app.core.auth as a
print("AUTH FILE BEING USED:", a.__file__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    email = decode_token(token)
    u = db.query(User).filter(User.email == email).first()
    if not u:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return u


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email}


@router.post("/signup", response_model=TokenOut)
def signup(data: SignupIn, db: Session = Depends(get_db)):
    print("DEBUG repr(password):", repr(data.password))
    print("DEBUG bytes length:", len(data.password.encode("utf-8")))
    u = User(email=data.email, password_hash=hash_password(data.password))
    db.add(u)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

    token = create_access_token(subject=u.email)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == data.email).first()
    if not u or not verify_password(data.password, u.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=u.email)
    return {"access_token": token, "token_type": "bearer"}
