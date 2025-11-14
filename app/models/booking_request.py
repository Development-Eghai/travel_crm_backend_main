from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from core.database import Base

class BookingRequest(Base):
    __tablename__ = "booking_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0)

    departure_date = Column(String(50), nullable=False)
    sharing_option = Column(String(50), nullable=False)
    price_per_person = Column(Integer, nullable=False)
    adults = Column(Integer, default=1)
    children = Column(Integer, default=0)
    estimated_total_price = Column(Integer, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)

    domain_name = Column(String(100), nullable=True)

    # NEW FIELD
    is_deleted = Column(Boolean, default=False)   # ← Soft delete column

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
