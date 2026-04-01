from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class ComplaintCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=5, max_length=50)
    county: str
    constituency: str
    category: str
    message: str = Field(min_length=5)


class ComplaintOut(BaseModel):
    id: int
    name: str
    phone: str
    county: str
    constituency: str
    category: str
    message: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LeaderOut(BaseModel):
    id: int
    name: str
    role: str
    county: str
    constituency: str
    party: str
    bio: str

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=500)


class SourceChunk(BaseModel):
    text: str
    source: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk] = []

class ComplaintStatusUpdate(BaseModel):
    status: str = Field(min_length=2, max_length=30)

class ProfileBase(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    county: Optional[str] = None
    constituency: Optional[str] = None
    ward: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class ProfileOut(ProfileBase):
    id: int

    class Config:
        from_attributes = True