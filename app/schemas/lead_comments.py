from pydantic import BaseModel
from datetime import datetime

class LeadCommentCreate(BaseModel):
    lead_id: int
    comment: str
    commented_by: int

class LeadCommentOut(BaseModel):
    id: int
    lead_id: int
    comment: str
    commented_by: int
    created_at: datetime

    class Config:
        from_attributes = True