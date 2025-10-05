from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, ForeignKey
from datetime import datetime
from core.database import Base

class QuotationItem(Base):
    __tablename__ = "quotation_items"

    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    quantity = Column(Integer, default=1)
    unit_price = Column(DECIMAL(12,2), default=0.0)
    total_price = Column(DECIMAL(12,2), default=0.0)
    sort_order = Column(Integer, default=0)
    tenant_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())