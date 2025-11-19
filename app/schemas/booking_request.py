from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class BookingRequestCreate(BaseModel):
    departure_date: str
    sharing_option: str
    price_per_person: int
    adults: int
    children: Optional[int] = 0
    estimated_total_price: int
    full_name: str
    email: EmailStr
    phone_number: str
    domain_name: Optional[str] = None


class BookingRequestOut(BookingRequestCreate):
    id: int
    booking_id: Optional[int] = None   # <-- NEW FIELD
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True
