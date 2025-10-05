from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date, time
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
    destination_type: str
    pickup: Optional[str]
    drop: Optional[str]
    travel_from: Optional[date]
    travel_to: Optional[date]
    adults: Optional[int]
    children: Optional[int]
    status: Optional[str] = "New"
    priority: Optional[str] = "Medium"
    assigned_to: Optional[int]
    follow_up_date: Optional[date]
    source: Optional[str]

    comments: Optional[List[LeadCommentIn]] = []
    linked_documents: Optional[List[LeadDocumentIn]] = []


class LeadOut(BaseModel):
    id: int
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
    status: str
    priority: str
    assigned_to: Optional[int]
    follow_up_date: Optional[date]
    created_at: datetime
    source: Optional[str]

    class Config:
        from_attributes = True