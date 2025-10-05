# app/models/blog_post.py
from sqlalchemy import Column, Integer, String, Text, JSON, Boolean, Date, DateTime
from datetime import datetime
from core.database import Base

class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    heading = Column(String(255), nullable=False)
    category_id = Column(Integer, nullable=True)
    featured_image = Column(Text, nullable=True)
    alt_tag = Column(Text, nullable=True)
    date = Column(Date, nullable=True)
    author_name = Column(String(255), nullable=True)
    tag_ids = Column(JSON, nullable=True)
    is_featured = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    meta_title = Column(String(255), nullable=True)
    meta_tag = Column(Text, nullable=True)
    meta_description = Column(Text, nullable=True)
    slug = Column(String(255), nullable=True)
    tenant_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())