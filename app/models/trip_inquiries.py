from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from core.database import Base

class TripInquiry(Base):
    __tablename__ = "trip_inquiries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0)     
    departure_date = Column(String(50), nullable=False)
    adults = Column(Integer, default=1)
    children = Column(Integer, default=0)
    children_ages = Column(String(100), nullable=True)  # Comma-separated ages
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)