from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
)
from sqlalchemy.sql import func
from core.database import Base


class EnquireForm(Base):
    __tablename__ = "enquire_form"

    id = Column(Integer, primary_key=True, autoincrement=True)
    destination = Column(String(100), nullable=False)
    departure_city = Column(String(100), nullable=False)
    travel_date = Column(String(50), nullable=False)
    adults = Column(Integer, default=1)
    children = Column(Integer, default=0)
    infants = Column(Integer, default=0)
    hotel_category = Column(String(50), nullable=True)
    full_name = Column(String(100), nullable=False)
    contact_number = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    additional_comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<EnquireForm(id={self.id}, name='{self.full_name}', destination='{self.destination}')>"


