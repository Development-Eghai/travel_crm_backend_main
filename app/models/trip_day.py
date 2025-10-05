# app/models/trip_day.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import JSON
from datetime import datetime
from core.database import Base

class TripDay(Base):
    __tablename__ = "trip_days"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    day_title = Column(String(255), nullable=False)
    image_url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    activity_ids = Column(JSON, nullable=True)  # List of activity IDs
    accommodation = Column(Text, nullable=True)
    tenant_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())