# app/schemas/category.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict,field_validator
from typing import Optional,List

class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[List[str]] = []
    tenant_id: int

    model_config = ConfigDict(from_attributes=True)

class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    image: Optional[List[str]] = []
    tenant_id: int

    class Config:
        from_attributes = True

    @field_validator("image", mode="before")
    @classmethod
    def parse_image(cls, value):
        if isinstance(value, str):
            return [value]
        return value
