# app/models/booking.py
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from datetime import datetime
from core.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(255), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)

    booking_type = Column(
        Enum("Fixed Departure", "Customized", name="booking_type_enum"),
        nullable=False
    )
    booking_status = Column(
        Enum("Pending", "Confirmed", "Cancelled", name="booking_status_enum"),
        default="Pending",
        nullable=False
    )
    payment_status = Column(
        Enum("Pending", "Paid", "Refunded", name="payment_status_enum"),
        default="Pending",
        nullable=False
    )

    tenant_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
