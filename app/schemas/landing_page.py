from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime, date

# ============= LANDING PAGE SUB-SCHEMAS =============

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
    emails: List[ContactInfo] = []
    phones: List[ContactInfo] = []
    addresses: List[AddressInfo] = []
    social_media: List[SocialMediaLink] = []
    business_hours: Optional[str] = ""


# ===== 4. TRIP PRICING (Multiple prices with currency support) =====
class TripPricing(BaseModel):
    """Individual price entry with label and currency"""
    price: float
    label: str = "Per Person"
    currency: str = "INR"
    is_offer: bool = False
    offer_price: Optional[float] = None

class TripInclusions(BaseModel):
    """Trip inclusions with icon checkboxes"""
    flight: bool = False
    hotels: bool = False
    sightseeing: bool = False
    meals: bool = False
    transfers: bool = False
    other_inclusions: str = ""


# ===== 5. UPDATED: CUSTOM TRIP CREATION =====
class CustomTrip(BaseModel):
    """
    Custom trip created directly in landing page
    
    UPDATED:
    - Added badge field
    - Renamed highlights to itinerary (keeping rich text format)
    """
    trip_title: str
    trip_images: List[str] = []
    badge: Optional[str] = ""  # NEW: Badge like "Popular", "Best Seller", "Hot Deal"
    inclusions: TripInclusions = TripInclusions()
    itinerary: str = ""  # RENAMED from highlights - Rich text editor content for day-wise itinerary
    pricing: List[TripPricing] = []
    additional_info: Optional[str] = ""  # Optional additional information


# ===== 6. CUSTOM PACKAGES =====
class CustomPackage(BaseModel):
    """Custom package grouping multiple trips or custom trips"""
    title: str
    description: str
    trip_ids: List[int] = []
    custom_trips: List[CustomTrip] = []
    badge: Optional[str] = ""
    discount_text: Optional[str] = ""


# ===== 7. PACKAGES SECTION =====
class Packages(BaseModel):
    """Packages section with custom packages and custom trips"""
    section_title: str = "Tour Packages"
    section_subtitle: str = "Explore our hand-picked packages"
    selected_trips: List['SelectedTrip'] = []
    custom_trips: List[CustomTrip] = []
    custom_packages: List[CustomPackage] = []
    show_section: bool = True


# ===== 8. NEW: WHY CHOOSE US SECTION =====
class WhyChooseUsItem(BaseModel):
    """Individual reason/benefit item"""
    title: str
    image: Optional[str] = ""  # Image URL
    icon: Optional[str] = ""   # Icon name (can use lucide-react icons)
    description: str

class WhyChooseUs(BaseModel):
    """
    Why Choose Us section
    Highlights company benefits, USPs, and competitive advantages
    """
    section_title: str = "Why Choose Us"
    section_subtitle: str = "What makes us different"
    items: List[WhyChooseUsItem] = []
    show_section: bool = True


# ===== 9. NEW: CUSTOM SECTIONS =====
class CustomSectionFormat1(BaseModel):
    """
    Format 1: Simple text-based section
    Section with title, subtitle, and rich text description
    """
    format_type: Literal["format_1"] = "format_1"
    section_title: str
    section_subtitle: str = ""
    description: str  # Rich text editor content

class CustomSectionItemFormat2(BaseModel):
    """Individual item for Format 2"""
    title: str
    image: Optional[str] = ""
    icon: Optional[str] = ""
    description: str

class CustomSectionFormat2(BaseModel):
    """
    Format 2: Item-based section
    Section with title, subtitle, and multiple items
    """
    format_type: Literal["format_2"] = "format_2"
    section_title: str
    section_subtitle: str = ""
    items: List[CustomSectionItemFormat2] = []

# Union type for custom sections
from typing import Union
CustomSectionContent = Union[CustomSectionFormat1, CustomSectionFormat2]

class CustomSection(BaseModel):
    """
    Custom section with ordering support
    Can be either Format 1 (text) or Format 2 (items)
    """
    id: str  # Unique identifier for reordering
    order: int = Field(ge=1, description="Display order")
    content: CustomSectionContent  # Either Format1 or Format2
    show_section: bool = True

class CustomSections(BaseModel):
    """Container for all custom sections with ordering"""
    sections: List[CustomSection] = []


# ===== 10. FOOTER SCHEMAS =====
class FooterColumn(BaseModel):
    """Individual footer column with rich text content"""
    title: str
    content: str
    order: int = Field(ge=1)
    status: str = "active"

class FooterSettings(BaseModel):
    """Footer-wide settings"""
    copyright_text: str = ""
    keywords: str = ""
    status: str = "active"

class Footer(BaseModel):
    """Complete footer structure"""
    columns: List[FooterColumn] = []
    settings: FooterSettings = FooterSettings()


# ===== 11. SECTION ORDER MANAGEMENT =====
class SectionOrder(BaseModel):
    """
    Defines the display order of all sections on the landing page
    Allows users to rearrange sections via drag & drop
    """
    section_name: str  # e.g., "hero", "packages", "why_choose_us", "custom_section_1"
    order: int = Field(ge=1)
    visible: bool = True

class SectionOrdering(BaseModel):
    """Container for section ordering configuration"""
    sections: List[SectionOrder] = []


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
    """Selected trip from existing database"""
    trip_id: int
    badge: Optional[str] = ""
    title: Optional[str] = ""
    slug: Optional[str] = ""
    days: Optional[int] = None
    nights: Optional[int] = None
    price: Optional[str] = ""
    hero_image: Optional[str] = ""
    highlights: Optional[List[str]] = []
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


# ============= MAIN LANDING PAGE SCHEMAS =============
class LandingPageBase(BaseModel):
    """
    Complete landing page structure with all sections
    
    NEW FEATURES:
    - Why Choose Us section
    - Custom Sections (Format 1 & Format 2)
    - Section ordering/reordering
    - Updated custom trips with badge and itinerary
    """
    page_name: str
    slug: str
    template: str = "template-one"
    is_active: bool = True
    
    # Core sections
    company: Optional[Company] = Company()
    company_about: Optional[CompanyAbout] = CompanyAbout()
    live_notifications: Optional[LiveBookingNotifications] = LiveBookingNotifications()
    footer: Optional[Footer] = Footer()
    
    # SEO and Hero
    seo: Optional[SEO] = SEO()
    hero: Hero
    
    # Main content sections
    packages: Optional[Packages] = Packages()
    why_choose_us: Optional[WhyChooseUs] = WhyChooseUs()  # NEW
    attractions: Optional[Attractions] = Attractions()
    gallery: Optional[Gallery] = Gallery()
    testimonials: Optional[Testimonials] = Testimonials()
    faqs: Optional[FAQs] = FAQs()
    travel_guidelines: Optional[TravelGuidelines] = TravelGuidelines()
    
    # NEW: Custom sections
    custom_sections: Optional[CustomSections] = CustomSections()
    
    # Offers and promotions
    offers: Optional[Offers] = Offers()
    
    # NEW: Section ordering
    section_order: Optional[SectionOrdering] = SectionOrdering()

class LandingPageCreate(LandingPageBase):
    pass

class LandingPageUpdate(BaseModel):
    page_name: Optional[str] = None
    slug: Optional[str] = None
    template: Optional[str] = None
    is_active: Optional[bool] = None
    company: Optional[Company] = None
    company_about: Optional[CompanyAbout] = None
    live_notifications: Optional[LiveBookingNotifications] = None
    footer: Optional[Footer] = None
    seo: Optional[SEO] = None
    hero: Optional[Hero] = None
    packages: Optional[Packages] = None
    why_choose_us: Optional[WhyChooseUs] = None  # NEW
    attractions: Optional[Attractions] = None
    gallery: Optional[Gallery] = None
    testimonials: Optional[Testimonials] = None
    faqs: Optional[FAQs] = None
    travel_guidelines: Optional[TravelGuidelines] = None
    custom_sections: Optional[CustomSections] = None  # NEW
    offers: Optional[Offers] = None
    section_order: Optional[SectionOrdering] = None  # NEW

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

# Rebuild to resolve forward references
Packages.model_rebuild()