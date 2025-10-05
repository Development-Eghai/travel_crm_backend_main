from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from datetime import datetime
from core.database import Base

class BlogCategory(Base):
    __tablename__ = "blog_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True)
    description = Column(Text)
    image_url = Column(Text)
    parent_id = Column(Integer, nullable=True)
    tenant_id = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    level = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())