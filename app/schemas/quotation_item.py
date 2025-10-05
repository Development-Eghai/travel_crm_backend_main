from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuotationItemBase(BaseModel):
    quotation_id: int
    title: str
    description: Optional[str]
    quantity: Optional[int] = 1
    unit_price: Optional[float] = 0.0
    total_price: Optional[float] = 0.0
    sort_order: Optional[int] = 0
    tenant_id: int

class QuotationItemCreate(QuotationItemBase):
    pass

class QuotationItemOut(QuotationItemBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True