from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class EnquireFormCreate(BaseModel):
    destination: str = Field(..., max_length=100)
    departure_city: str = Field(..., max_length=100)
    travel_date: str = Field(..., max_length=50)
    adults: Optional[int] = 1
    children: Optional[int] = 0
    infants: Optional[int] = 0
    hotel_category: Optional[str] = Field(None, max_length=50)
    full_name: str = Field(..., max_length=100)
    contact_number: str = Field(..., max_length=20)
    email: EmailStr
    additional_comments: Optional[str] = None

class EnquireFormOut(BaseModel):
    id: int
    destination: str
    departure_city: str
    travel_date: str
    adults: int
    children: Optional[int]
    infants: Optional[int]
    hotel_category: Optional[str]
    full_name: str
    contact_number: str
    email: EmailStr
    additional_comments: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ✅ Enables ORM model parsing

