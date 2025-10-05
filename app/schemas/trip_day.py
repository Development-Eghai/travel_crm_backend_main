# app/schemas/trip_day.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TripDayBase(BaseModel):
    trip_id: int
    day_title: str
    image_url: Optional[str]
    description: Optional[str]
    activity_ids: Optional[List[int]]  # JSON list of activity IDs
    accommodation: Optional[str]
    tenant_id: int

class TripDayCreate(TripDayBase):
    pass

class TripDayOut(TripDayBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True