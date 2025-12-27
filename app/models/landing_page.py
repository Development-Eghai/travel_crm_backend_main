from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, JSON, Index
from sqlalchemy.sql import func
from core.database import Base

class LandingPage(Base):
    __tablename__ = "landing_pages"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Basic Information
    page_name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    template = Column(String(50), default='template-one')
    is_active = Column(Boolean, default=True, index=True)
    
    # Multi-tenancy
    user_id = Column(Integer, nullable=False, index=True)
    domain_name = Column(String(255), nullable=False, index=True)
    
    # ===== JSON Data Columns =====
    
    # NEW: Global theme colors
    theme_colors = Column(JSON)
    
    # UPDATED: Enhanced company information (multiple emails, phones, addresses)
    company = Column(JSON)
    
    # NEW: Company about section (logo, team, highlights)
    company_about = Column(JSON)
    
    # NEW: Live booking notifications (Social Proof Widget)
    live_notifications = Column(JSON)
    
    # Existing JSON columns
    seo = Column(JSON)
    hero = Column(JSON)
    
    # UPDATED: Packages (now includes custom_packages array)
    packages = Column(JSON)
    
    attractions = Column(JSON)
    gallery = Column(JSON)
    testimonials = Column(JSON)
    faqs = Column(JSON)
    travel_guidelines = Column(JSON)
    offers = Column(JSON)
    
    # Analytics
    views = Column(Integer, default=0)
    leads = Column(Integer, default=0)
    
    # Soft Delete
    is_deleted = Column(Boolean, default=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Composite Index for better query performance
    __table_args__ = (
        Index('idx_user_domain_deleted', 'user_id', 'domain_name', 'is_deleted'),
    )