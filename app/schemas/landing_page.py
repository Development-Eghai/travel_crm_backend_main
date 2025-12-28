from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime, date

# ============= SUB-SCHEMAS =============

# ===== 1. LIVE BOOKING NOTIFICATIONS (Social Proof Widget) =====
class BookingNotification(BaseModel):
    """Single booking notification entry"""
    name: str
    location: str
    destination: str
    time: str

class LiveBookingNotifications(BaseModel):
    """Live booking notification popups (Social Proof)"""
    enabled: bool = True
    notifications: List[BookingNotification] = []
    display_duration: int = 5
    interval_between: int = 10
    position: str = "bottom-left"
    show_on_mobile: bool = True


# ===== 2. COMPANY ABOUT SECTION =====
class Highlight(BaseModel):
    """Individual highlight item with icon and text"""
    text: str
    icon: Optional[str] = "star"

class TeamMember(BaseModel):
    """Team member information"""
    name: str
    role: str
    image: str
    bio: Optional[str] = ""
    social_links: Optional[Dict[str, str]] = {}

class CompanyAbout(BaseModel):
    """Complete About Us section"""
    section_title: str = "About Us"
    section_subtitle: str = "Your Trusted Travel Partner"
    logo: str = ""
    heading: str = "Crafting Unforgettable Journeys"
    tagline: str = "Since 2015"
    description: str = ""
    highlights: List[Highlight] = []
    team_members: List[TeamMember] = []
    show_section: bool = True


# ===== 3. ENHANCED COMPANY INFO =====
class ContactInfo(BaseModel):
    """Single contact entry with value and label"""
    value: str
    label: Optional[str] = ""

class AddressInfo(BaseModel):
    """Address with optional map link"""
    label: Optional[str] = "Head Office"
    street: str
    city: str
    state: str
    country: str
    postal_code: str
    map_link: Optional[str] = ""
    is_primary: bool = False

class SocialMediaLink(BaseModel):
    """Social media link"""
    platform: str
    url: str
    icon: Optional[str] = ""

class Company(BaseModel):
    """Enhanced company information"""
    name: str = ""
    tagline: Optional[str] = ""
    logo: Optional[str] = ""
    
    # Contact info as objects with value and label
    emails: List[ContactInfo] = []
    phones: List[ContactInfo] = []
    
    # Addresses as objects with map link support
    addresses: List[AddressInfo] = []
    
    social_media: List[SocialMediaLink] = []
    business_hours: Optional[str] = ""


# ===== 4. CUSTOM PACKAGES =====
class CustomPackage(BaseModel):
    """Custom package grouping multiple trips"""
    title: str
    description: str
    trip_ids: List[int]
    badge: Optional[str] = ""
    discount_text: Optional[str] = ""

class Packages(BaseModel):
    """Updated packages section with custom packages"""
    section_title: str = "Tour Packages"
    section_subtitle: str = "Explore our hand-picked packages"
    selected_trips: List['SelectedTrip'] = []
    custom_packages: List[CustomPackage] = []
    show_section: bool = True


# ===== REMOVED: Theme colors section is now hidden =====


# ===== EXISTING SCHEMAS =====
class SEO(BaseModel):
    meta_title: Optional[str] = ""
    meta_description: Optional[str] = ""
    meta_tags: Optional[str] = ""
    og_image: Optional[str] = ""

class CTAButton(BaseModel):
    text: str = "Book Now"
    link: str = ""
    style: Optional[str] = "primary"

class Hero(BaseModel):
    title: str
    subtitle: Optional[str] = ""
    description: Optional[str] = ""
    cta_button_1: CTAButton = CTAButton()
    cta_button_2: CTAButton = CTAButton()
    background_type: Optional[str] = "slider"
    background_images: List[str] = []
    background_videos: List[str] = []
    overlay_opacity: Optional[float] = 0.4

class SelectedTrip(BaseModel):
    """Selected trip with flexible fields"""
    trip_id: int
    badge: Optional[str] = ""
    title: Optional[str] = ""
    slug: Optional[str] = ""
    days: Optional[int] = None
    nights: Optional[int] = None
    price: Optional[str] = ""  # STRING for price
    hero_image: Optional[str] = ""
    highlights: Optional[List[str]] = []  # Array of strings
    pricing_model: Optional[str] = ""
    image: Optional[str] = ""

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
    """Testimonial item"""
    name: str
    destination: str
    rating: int = Field(ge=1, le=5)
    description: str
    image: Optional[str] = ""
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
    background_color: Optional[str] = ""
    text_color: Optional[str] = ""

class MidSection(BaseModel):
    enabled: bool = False
    type: str = "image"
    media_urls: List[str] = []

class PopupConfig(BaseModel):
    enabled: bool = False
    title: str = ""
    description: Optional[str] = ""
    image: Optional[str] = ""
    cta_text: Optional[str] = "Get Offer"
    cta_link: Optional[str] = ""

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
    
    # theme_colors REMOVED - hidden for now
    company: Optional[Company] = Company()
    company_about: Optional[CompanyAbout] = CompanyAbout()
    live_notifications: Optional[LiveBookingNotifications] = LiveBookingNotifications()
    
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
    # theme_colors REMOVED
    company: Optional[Company] = None
    company_about: Optional[CompanyAbout] = None
    live_notifications: Optional[LiveBookingNotifications] = None
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

Packages.model_rebuild()