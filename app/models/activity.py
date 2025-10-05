from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from core.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    description = Column(Text)
    image = Column(Text)
    tenant_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())