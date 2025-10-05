# app/models/tag.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime
from core.database import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=True)
    description = Column(Text, nullable=True)
    tenant_id = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())