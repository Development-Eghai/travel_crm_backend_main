# app/schemas/fixed_departure.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FixedDepartureBase(BaseModel):
    trip_id: int
    title: str
    start_date: datetime
    end_date: datetime
    description: Optional[str]
    tenant_id: int

class FixedDepartureCreate(FixedDepartureBase):
    pass

class FixedDepartureOut(FixedDepartureBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True