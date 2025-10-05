# app/schemas/category.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    tenant_id: int

    model_config = ConfigDict(from_attributes=True)

class CategoryOut(CategoryCreate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
