# app/models/role.py
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from core.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    modules = Column(JSON, nullable=True)  # e.g. {"bookings": true, "leads": false}
    tenant_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())