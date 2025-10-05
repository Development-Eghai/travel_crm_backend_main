# app/schemas/blog_post.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class BlogPostBase(BaseModel):
    heading: str
    category_id: Optional[int]
    featured_image: Optional[str]
    alt_tag: Optional[str]
    date: Optional[date]
    author_name: Optional[str]
    tag_ids: Optional[List[int]] = []
    is_featured: Optional[bool] = False
    is_published: Optional[bool] = False
    description: Optional[str]
    meta_title: Optional[str]
    meta_tag: Optional[str]
    meta_description: Optional[str]
    slug: Optional[str]
    tenant_id: int

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostOut(BlogPostBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True