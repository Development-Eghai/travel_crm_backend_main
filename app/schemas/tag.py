# app/schemas/tag.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TagBase(BaseModel):
    name: str
    slug: Optional[str]
    description: Optional[str]
    tenant_id: int
    is_active: Optional[bool] = True

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True