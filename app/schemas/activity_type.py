# app/schemas/activity_type.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActivityTypeBase(BaseModel):
    name: str
    description: Optional[str]
    icon_url: Optional[str]
    tenant_id: int
    is_active: Optional[bool] = True

class ActivityTypeCreate(ActivityTypeBase):
    pass

class ActivityTypeOut(ActivityTypeBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True