from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TripTypeCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    tenant_id: int

    model_config = ConfigDict(from_attributes=True)

class TripTypeOut(TripTypeCreate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]