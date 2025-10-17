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

class BookingRequestOut(BookingRequestCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True