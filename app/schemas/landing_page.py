from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date

# ============= SUB-SCHEMAS =============

class SocialMedia(BaseModel):
    facebook: Optional[str] = ""
    instagram: Optional[str] = ""
    twitter: Optional[str] = ""
    youtube: Optional[str] = ""

class Company(BaseModel):
    name: Optional[str] = ""
    contact: Optional[str] = ""
    social_media: Optional[SocialMedia] = SocialMedia()

class SEO(BaseModel):
    meta_title: Optional[str] = ""
    meta_description: Optional[str] = ""
    meta_tags: Optional[str] = ""

class CTAButton(BaseModel):
    text: str = "Book Now"
    link: str = ""

class Hero(BaseModel):
    title: str
    subtitle: Optional[str] = ""
    description: Optional[str] = ""
    cta_button_1: CTAButton = CTAButton()
    cta_button_2: CTAButton = CTAButton()
    background_type: Optional[str] = "slider"  # Added this field from frontend
    background_images: List[str] = []
    background_videos: List[str] = []

class SelectedTrip(BaseModel):
    trip_id: int
    badge: str = ""
    trip_title: str = ""
    price: str = ""
    pricing_model: Optional[str] = ""
    image: Optional[str] = ""

class Packages(BaseModel):
    section_title: str = "Popular Tour Packages"
    section_subtitle: str = "Explore our hand-picked packages"
    selected_trips: List[SelectedTrip] = []
    show_section: bool = True

class AttractionItem(BaseModel):
    title: str
    image: str
    description: str

class Attractions(BaseModel):
    section_title: str = "Top Attractions"
    section_subtitle: str = "Must-visit places"
    items: List[AttractionItem] = []
    show_section: bool = True

class Gallery(BaseModel):
    section_title: str = "Photo Gallery"
    section_subtitle: str = "Captured moments"
    images: List[str] = []
    videos: List[str] = []
    show_section: bool = True

class TestimonialItem(BaseModel):
    name: str
    destination: str
    rating: int = Field(ge=1, le=5)
    description: str
    image: str
    date: str

class Testimonials(BaseModel):
    section_title: str = "What Our Travelers Say"
    section_subtitle: str = "Real experiences"
    items: List[TestimonialItem] = []
    show_section: bool = True

class FAQItem(BaseModel):
    question: str
    answer: str

class FAQs(BaseModel):
    section_title: str = "Frequently Asked Questions"
    section_subtitle: str = "Everything you need to know"
    items: List[FAQItem] = []
    show_section: bool = True

class TravelGuidelines(BaseModel):
    section_title: str = "Travel Guidelines"
    section_subtitle: str = "Important information"
    description: str = ""
    show_section: bool = True

class BannerConfig(BaseModel):
    enabled: bool = False
    text: str = ""

class MidSection(BaseModel):
    enabled: bool = False
    type: str = "image"  # 'image' or 'video'
    media_urls: List[str] = []  # Changed from media_url to media_urls (array)

class PopupConfig(BaseModel):
    enabled: bool = False
    title: str = ""

class Popups(BaseModel):
    entry: PopupConfig = PopupConfig()
    exit: PopupConfig = PopupConfig()
    idle: PopupConfig = PopupConfig()

class Offers(BaseModel):
    start_date: str = ""
    end_date: str = ""
    header: BannerConfig = BannerConfig()
    footer: BannerConfig = BannerConfig()
    mid_section: MidSection = MidSection()
    popups: Popups = Popups()

# ============= MAIN SCHEMAS =============

class LandingPageBase(BaseModel):
    page_name: str
    slug: str
    template: str = "template-one"
    is_active: bool = True
    company: Optional[Company] = Company()
    seo: Optional[SEO] = SEO()
    hero: Hero
    packages: Optional[Packages] = Packages()
    attractions: Optional[Attractions] = Attractions()
    gallery: Optional[Gallery] = Gallery()
    testimonials: Optional[Testimonials] = Testimonials()
    faqs: Optional[FAQs] = FAQs()
    travel_guidelines: Optional[TravelGuidelines] = TravelGuidelines()
    offers: Optional[Offers] = Offers()

class LandingPageCreate(LandingPageBase):
    pass

class LandingPageUpdate(BaseModel):
    page_name: Optional[str] = None
    slug: Optional[str] = None
    template: Optional[str] = None
    is_active: Optional[bool] = None
    company: Optional[Company] = None
    seo: Optional[SEO] = None
    hero: Optional[Hero] = None
    packages: Optional[Packages] = None
    attractions: Optional[Attractions] = None
    gallery: Optional[Gallery] = None
    testimonials: Optional[Testimonials] = None
    faqs: Optional[FAQs] = None
    travel_guidelines: Optional[TravelGuidelines] = None
    offers: Optional[Offers] = None

class LandingPageResponse(LandingPageBase):
    id: int
    user_id: int
    domain_name: str
    views: int = 0
    leads: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class LandingPageList(BaseModel):
    id: int
    page_name: str
    slug: str
    template: str
    is_active: bool
    views: int
    leads: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PaginatedLandingPages(BaseModel):
    pages: List[LandingPageList]
    total: int
    page: int
    per_page: int
    total_pages: int