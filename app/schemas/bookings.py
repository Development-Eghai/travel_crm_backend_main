# app/schemas/booking.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal

class BookingCreate(BaseModel):
    customer_name: str
    trip_id: int
    booking_type: Literal["Fixed Departure", "Customized"]
    booking_status: Optional[Literal["Pending", "Confirmed", "Cancelled"]] = "Pending"
    payment_status: Optional[Literal["Pending", "Paid", "Refunded"]] = "Pending"
    tenant_id: int

    model_config = ConfigDict(from_attributes=True)

class BookingOut(BookingCreate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
