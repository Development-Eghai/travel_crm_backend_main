from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ------------------------------------------------------
# CREATE SCHEMA
# ------------------------------------------------------
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

    # used only for CREATE to identify tenant
    domain_name: Optional[str] = None


# ------------------------------------------------------
# UPDATE SCHEMA (ALL FIELDS OPTIONAL)
# ------------------------------------------------------
class BookingRequestUpdate(BaseModel):
    departure_date: Optional[str] = None
    sharing_option: Optional[str] = None
    price_per_person: Optional[int] = None
    adults: Optional[int] = None
    children: Optional[int] = None
    estimated_total_price: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    class Config:
        extra = "forbid"


# ------------------------------------------------------
# OUTPUT SCHEMA
# ------------------------------------------------------
class BookingRequestOut(BookingRequestCreate):
    id: int
    booking_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True
