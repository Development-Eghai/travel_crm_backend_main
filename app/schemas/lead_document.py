from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LeadDocumentOut(BaseModel):
    id: int
    lead_id: int
    file_name: str
    file_path: str
    uploaded_by: Optional[int]
    uploaded_at: datetime

    class Config:
        from_attributes = True