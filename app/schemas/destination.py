from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class CustomPackageSchema(BaseModel):
    title: str
    description: Optional[str]
    trip_ids: List[int]

class DestinationCreate(BaseModel):
    title: str
    subtitle: Optional[str]
    destination_type: str
    primary_destination_id: Optional[int]
    slug: Optional[str]
    overview: Optional[str]
    travel_guidelines: Optional[str]
    popular_trip_ids: List[int]
    custom_packages: List[CustomPackageSchema]
    blog_category_ids: List[int]
    featured_blog_ids: List[int]
    activity_ids: List[int]
    testimonial_ids: List[int]
    related_blog_ids: List[int]

class CustomPackageOut(BaseModel):
    title: str
    description: Optional[str]
    trip_ids: List[int]

class DestinationOut(BaseModel):
    id: int
    title: str
    subtitle: Optional[str]
    destination_type: str
    primary_destination_id: Optional[int]
    slug: str
    overview: Optional[str]
    travel_guidelines: Optional[str]
    created_at: datetime
    updated_at: datetime

    # Related fields as flat lists of IDs
    popular_trip_ids: List[int] = []
    custom_packages: List[CustomPackageOut] = []
    blog_category_ids: List[int] = []
    featured_blog_ids: List[int] = []
    related_blog_ids: List[int] = []
    activity_ids: List[int] = []
    testimonial_ids: List[int] = []

    class Config:
        from_attributes = True
        from_attributes = True

