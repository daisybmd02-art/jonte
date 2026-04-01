from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class ProfileBase(BaseModel):
    model_config = ConfigDict(extra="ignore")
    full_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    county: str
    constituency: str
    ward: str
    lat: Optional[float] = None
    lng: Optional[float] = None


class ProfileOut(ProfileBase):
    id: int

    class Config:
        from_attributes = True
