from pydantic import BaseModel, EmailStr,field_validator

from typing import Optional, List
from datetime import datetime

class TripInquiryCreate(BaseModel):
    departure_date: str
    adults: int
    children: Optional[int] = 0
    children_ages: Optional[List[int]] = []
    full_name: str
    email: EmailStr
    phone_number: str

class TripInquiryOut(BaseModel):
    id: int
    departure_date: str
    adults: int
    children: Optional[int]
    children_ages: Optional[List[int]] = []
    full_name: str
    email: EmailStr
    phone_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_validator("children_ages", mode="before")
    @classmethod
    def parse_children_ages(cls, value):
        if isinstance(value, str):
            return [int(age.strip()) for age in value.split(",") if age.strip().isdigit()]
        return value
