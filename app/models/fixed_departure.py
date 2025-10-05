# app/models/fixed_departure.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from core.database import Base

class FixedDeparture(Base):
    __tablename__ = "fixed_departures"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    title = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    description = Column(Text, nullable=True)
    tenant_id = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())