from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BlogCategoryBase(BaseModel):
    name: str
    slug: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    parent_id: Optional[int]
    tenant_id: int
    is_active: Optional[bool] = True
    sort_order: Optional[int] = 0
    level: Optional[int] = 0

class BlogCategoryCreate(BlogCategoryBase):
    pass

class BlogCategoryOut(BlogCategoryBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True