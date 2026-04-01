from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status

SECRET_KEY = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def _bcrypt_safe(password) -> str:
    print("DEBUG type:", type(password))
    print("DEBUG repr:", repr(password))

    # force to string just for debugging
    if not isinstance(password, str):
        password = str(password)

    print("DEBUG bytes:", len(password.encode("utf-8")))

    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400, detail="Password too long (max 72 bytes).")
    return password


def hash_password(password: str) -> str:
    password = _bcrypt_safe(password)
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    password = _bcrypt_safe(password)
    return pwd_context.verify(password, hashed)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        if not sub:
            raise JWTError("Missing sub")
        return sub
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
