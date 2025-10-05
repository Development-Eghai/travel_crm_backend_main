from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# ---------- Activity ----------
class ActivityCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str]
    image: Optional[str]
    tenant_id: int
    model_config = ConfigDict(from_attributes=True)

class ActivityOut(ActivityCreate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

# ---------- Trip Type ----------
class TripTypeCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str]
    image: Optional[str]
    tenant_id: int
    model_config = ConfigDict(from_attributes=True)

class TripTypeOut(TripTypeCreate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

# ---------- Destination ----------
class DestinationCreate(BaseModel):
    name: str
    slug: str
    hero_image: Optional[str]
    description: Optional[str]
    parent_id: Optional[int]
    destination_type: str  # "Domestic" or "International"
    popular_trip_ids: Optional[List[int]]
    blog_category_ids: Optional[List[int]]
    featured_blog_ids: Optional[List[int]]
    about: Optional[str]
    how_to_reach: Optional[str]
    activity_ids: Optional[List[int]]
    travel_guide_tips: Optional[str]
    tenant_id: int
    model_config = ConfigDict(from_attributes=True)

class DestinationOut(DestinationCreate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

# ---------- Category ----------
class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str]
    image: Optional[str]
    tenant_id: int
    model_config = ConfigDict(from_attributes=True)

class CategoryOut(CategoryCreate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]