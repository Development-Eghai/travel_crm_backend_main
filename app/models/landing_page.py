from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, JSON, Index
from sqlalchemy.sql import func
from core.database import Base


class LandingPage(Base):
    """
    Landing Page Model - Complete Structure
    
    NEW FEATURES:
    - Custom Scripts for tracking/analytics (Google Analytics, Meta Pixel, etc.)
    - Custom trips with badge support
    - Itinerary field for day-wise details
    - Why Choose Us section
    - Custom sections (Format 1 & Format 2)
    - Section ordering (optional - hidden from basic UI)
    
    All sections stored as JSON for maximum flexibility
    """
    __tablename__ = "landing_pages"
    
    # ===== PRIMARY KEY =====
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # ===== BASIC INFORMATION =====
    page_name = Column(String(255), nullable=False, comment="Landing page name")
    slug = Column(String(255), unique=True, nullable=False, index=True, comment="URL slug")
    template = Column(String(50), default='template-one', comment="Template variant")
    is_active = Column(Boolean, default=True, index=True, comment="Published status")
    
    # ===== MULTI-TENANCY =====
    user_id = Column(Integer, nullable=False, index=True, comment="Owner user ID")
    domain_name = Column(String(255), nullable=False, index=True, comment="Domain identifier")
    
    # ===== JSON DATA COLUMNS =====
    
    # NEW: Custom Scripts (Tracking & Analytics)
    custom_scripts = Column(JSON, comment="""
        Custom tracking scripts (Google Analytics, Meta Pixel, etc.)
        Structure:
        {
            "scripts": [
                {
                    "id": "ga4_001",
                    "name": "Google Analytics 4",
                    "script_code": "<script>...</script>",
                    "location": "head",
                    "enabled": true,
                    "order": 1
                }
            ]
        }
    """)
    
    # Theme and branding
    theme_colors = Column(JSON, comment="Color scheme configuration")
    company = Column(JSON, comment="Company information: name, logo, contacts, addresses")
    company_about = Column(JSON, comment="About us: heading, description, team members")
    
    # Dynamic features
    live_notifications = Column(JSON, comment="Social proof booking notifications")
    footer = Column(JSON, comment="Footer columns, copyright, keywords")
    
    # SEO and hero
    seo = Column(JSON, comment="Meta tags, OG tags, SEO metadata")
    hero = Column(JSON, comment="Hero section: title, CTAs, background media")
    
    # Main content sections
    packages = Column(JSON, comment="""
        Tour packages with custom trips
        Structure:
        {
            "custom_trips": [
                {
                    "trip_title": "...",
                    "badge": "Popular",
                    "itinerary": "<p>Day 1: ...</p>",
                    "pricing": [...],
                    "inclusions": {...}
                }
            ]
        }
    """)
    
    why_choose_us = Column(JSON, comment="""
        Why Choose Us section
        Structure:
        {
            "section_title": "Why Choose Us",
            "section_subtitle": "...",
            "items": [
                {
                    "title": "Best Prices",
                    "icon": "dollar-sign",
                    "image": "url",
                    "description": "..."
                }
            ],
            "show_section": true
        }
    """)
    
    attractions = Column(JSON, comment="Top attractions with images")
    gallery = Column(JSON, comment="Photo and video gallery")
    testimonials = Column(JSON, comment="Customer testimonials with ratings")
    faqs = Column(JSON, comment="Frequently asked questions")
    travel_guidelines = Column(JSON, comment="Travel guidelines and tips")
    
    custom_sections = Column(JSON, comment="""
        User-created custom sections
        Structure:
        {
            "sections": [
                {
                    "id": "custom_1",
                    "order": 1,
                    "content": {
                        "format_type": "format_1",
                        "section_title": "...",
                        "description": "<p>Rich text</p>"
                    },
                    "show_section": true
                }
            ]
        }
    """)
    
    offers = Column(JSON, comment="Promotional offers, banners, popups")
    
    section_order = Column(JSON, nullable=True, comment="""
        [OPTIONAL/HIDDEN] Section display order configuration
        Only used when drag-drop reordering is needed
        Structure:
        {
            "sections": [
                {"section_name": "hero", "order": 1, "visible": true}
            ]
        }
    """)
    
    # ===== ANALYTICS =====
    views = Column(Integer, default=0, comment="Total page views")
    leads = Column(Integer, default=0, comment="Total lead conversions")
    
    # ===== SOFT DELETE =====
    is_deleted = Column(Boolean, default=False, index=True, comment="Soft delete flag")
    
    # ===== TIMESTAMPS =====
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # ===== INDEXES =====
    __table_args__ = (
        Index('idx_user_domain_deleted', 'user_id', 'domain_name', 'is_deleted'),
    )