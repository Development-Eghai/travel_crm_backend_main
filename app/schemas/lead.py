from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date

class LeadCommentIn(BaseModel):
    user_name: str
    comment: str

class LeadDocumentIn(BaseModel):
    file_name: str
    file_path: str
    uploaded_by: int
    uploaded_at: datetime


class LeadCreate(BaseModel):
    name: str
    email: str
    mobile: str
    destination_type: int
    pickup: str
    drop: str
    travel_from: datetime
    travel_to: datetime
    adults: str
    children: str


class LeadOut(BaseModel):
    id: int
    lead_id: Optional[int] = None   # <-- NEW FIELD
    user_id: int

    name: str
    email: str
    mobile: str
    destination_type: str
    pickup: Optional[str]
    drop: Optional[str]
    travel_from: Optional[date]
    travel_to: Optional[date]
    adults: Optional[int]
    children: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
