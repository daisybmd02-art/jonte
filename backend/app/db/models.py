from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from app.db.session import Base
from sqlalchemy.orm import relationship, synonym
from sqlalchemy import ForeignKey


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),
                     unique=True, nullable=False)

    full_name = Column(String(120), nullable=True)
    phone = Column(String(40), nullable=True)

    county = Column(String(120), nullable=True)
    constituency = Column(String(120), nullable=True)
    ward = Column(String(120), nullable=True)
    # <-- add email if you want it stored
    email = Column(String(120), nullable=True)

    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=True)
    phone = Column(String(40), nullable=True)

    county = Column(String(120), nullable=True)
    constituency = Column(String(120), nullable=True)
    ward = Column(String(120), nullable=True)  # ✅ add

    category = Column(String(80), nullable=False, default="Service delivery")
    message = Column(Text, nullable=False)

    # ✅ routing fields (not a person)
    # WARD/CONSTITUENCY/COUNTY/NATIONAL
    routing_level = Column(String(20), nullable=True)
    # e.g. "County Health Department"
    target_office = Column(String(120), nullable=True)

    status = Column(String(30), nullable=False, default="submitted")
    created_at = Column(DateTime, default=datetime.utcnow)


class Leader(Base):
    __tablename__ = "leaders"

    id = Column(Integer, primary_key=True, index=True)

    # Keep "name" because your routers already use Leader.name
    name = Column(String(120), nullable=False, index=True)

    # Optional: allow using Leader.full_name too (won’t create a new column)
    full_name = synonym("name")

    role = Column(String(80), nullable=False, index=True)
    party = Column(String(80), nullable=True)

    # NATIONAL | COUNTY | CONSTITUENCY | WARD
    level = Column(String(20), nullable=True, index=True)
    county = Column(String(80), nullable=True, index=True)
    constituency = Column(String(80), nullable=True, index=True)
    ward = Column(String(80), nullable=True, index=True)

    photo_url = Column(Text, nullable=True)
    image_path = Column(Text, nullable=True)   # ✅ add this
    # Keep "bio" because your seeder uses bio
    bio = Column(Text, nullable=True)

    # Optional: support these too if you want later (does NOT break old code)
    work_summary = Column(Text, nullable=True)
    achievements = Column(Text, nullable=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
