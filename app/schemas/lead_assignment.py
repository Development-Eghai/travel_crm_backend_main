# app/schemas/lead_assignment.py
from pydantic import BaseModel
from datetime import datetime,date
from typing import Optional

class LeadAssignmentBase(BaseModel):
    lead_id: int
    assigned_to: int
    due_date: date
    priority: str
    follow_up_date: date
    comments: Optional[str]
    tenant_id: int

class LeadAssignmentCreate(LeadAssignmentBase):
    pass

class LeadAssignmentOut(LeadAssignmentBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True