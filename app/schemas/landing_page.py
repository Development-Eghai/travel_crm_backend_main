from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any, Literal, Union
from datetime import datetime


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


# ===== 4. TRIP PRICING =====
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


# ===== 5. CUSTOM TRIP CREATION =====
class CustomTrip(BaseModel):
    """Custom trip created directly in landing page"""
    trip_title: str
    trip_images: List[str] = []
    badge: Optional[str] = ""
    inclusions: TripInclusions = TripInclusions()
    itinerary: str = ""
    pricing: List[TripPricing] = []
    additional_info: Optional[str] = ""


# ===== 6. CUSTOM PACKAGES =====
class CustomPackage(BaseModel):
    """Custom package grouping multiple trips or custom trips"""
    title: str
    description: str
    trip_ids: List[int] = []
    custom_trips: List[CustomTrip] = []
    badge: Optional[str] = ""
    discount_text: Optional[str] = ""


# ===== 7. SELECTED TRIP =====
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


# ===== 8. PACKAGES SECTION =====
class Packages(BaseModel):
    """Packages section with custom packages and custom trips"""
    section_title: str = "Tour Packages"
    section_subtitle: str = "Explore our hand-picked packages"
    selected_trips: List[SelectedTrip] = []
    custom_trips: List[CustomTrip] = []
    custom_packages: List[CustomPackage] = []
    show_section: bool = True


# ===== 9. WHY CHOOSE US SECTION =====
class WhyChooseUsItem(BaseModel):
    """Individual reason/benefit item"""
    title: str
    image: Optional[str] = ""
    icon: Optional[str] = ""
    description: str


class WhyChooseUs(BaseModel):
    """Why Choose Us section highlighting company benefits and USPs"""
    section_title: str = "Why Choose Us"
    section_subtitle: str = "What makes us different"
    items: List[WhyChooseUsItem] = []
    show_section: bool = True


# ===== 10. CUSTOM SECTIONS =====
class CustomSectionFormat1(BaseModel):
    """Format 1: Simple text-based section"""
    format_type: Literal["format_1"] = "format_1"
    section_title: str
    section_subtitle: str = ""
    description: str


class CustomSectionItemFormat2(BaseModel):
    """Individual item for Format 2"""
    title: str
    image: Optional[str] = ""
    icon: Optional[str] = ""
    description: str


class CustomSectionFormat2(BaseModel):
    """Format 2: Item-based section"""
    format_type: Literal["format_2"] = "format_2"
    section_title: str
    section_subtitle: str = ""
    items: List[CustomSectionItemFormat2] = []


CustomSectionContent = Union[CustomSectionFormat1, CustomSectionFormat2]


class CustomSection(BaseModel):
    """Custom section with ordering support"""
    id: str
    order: int = Field(ge=1, description="Display order")
    content: CustomSectionContent
    show_section: bool = True


class CustomSections(BaseModel):
    """Container for all custom sections"""
    sections: List[CustomSection] = []


# ===== 11. ATTRACTIONS =====
class AttractionItem(BaseModel):
    """Individual attraction"""
    title: str
    image: str
    description: str


class Attractions(BaseModel):
    """Top attractions section"""
    section_title: str = "Top Attractions"
    section_subtitle: str = "Must-visit places"
    items: List[AttractionItem] = []
    show_section: bool = True


# ===== 12. GALLERY =====
class Gallery(BaseModel):
    """Photo and video gallery"""
    section_title: str = "Photo Gallery"
    section_subtitle: str = "Captured moments"
    images: List[str] = []
    videos: List[str] = []
    show_section: bool = True


# ===== 13. TESTIMONIALS =====
class TestimonialItem(BaseModel):
    """Testimonial item"""
    name: str
    destination: str
    rating: int = Field(ge=1, le=5)
    description: str
    image: Optional[str] = ""
    date: str


class Testimonials(BaseModel):
    """Testimonials section"""
    section_title: str = "What Our Travelers Say"
    section_subtitle: str = "Real experiences"
    items: List[TestimonialItem] = []
    show_section: bool = True


# ===== 14. FAQs =====
class FAQItem(BaseModel):
    """FAQ item"""
    question: str
    answer: str


class FAQs(BaseModel):
    """Frequently asked questions section"""
    section_title: str = "Frequently Asked Questions"
    section_subtitle: str = "Everything you need to know"
    items: List[FAQItem] = []
    show_section: bool = True


# ===== 15. TRAVEL GUIDELINES =====
class TravelGuidelines(BaseModel):
    """Travel guidelines section"""
    section_title: str = "Travel Guidelines"
    section_subtitle: str = "Important information"
    description: str = ""
    show_section: bool = True


# ===== 16. FOOTER =====
class FooterColumn(BaseModel):
    """Individual footer column"""
    title: str
    content: str
    order: int = Field(ge=1)
    status: str = "active"


class FooterSettings(BaseModel):
    """Footer settings"""
    copyright_text: str = ""
    keywords: str = ""
    status: str = "active"


class Footer(BaseModel):
    """Complete footer structure"""
    columns: List[FooterColumn] = []
    settings: FooterSettings = FooterSettings()


# ===== 17. SEO =====
class SEO(BaseModel):
    """SEO metadata"""
    meta_title: Optional[str] = ""
    meta_description: Optional[str] = ""
    meta_tags: Optional[str] = ""
    og_image: Optional[str] = ""


# ===== 18. HERO SECTION =====
class CTAButton(BaseModel):
    """Call-to-action button"""
    text: str = "Book Now"
    link: str = ""
    style: Optional[str] = "primary"


class Hero(BaseModel):
    """Hero section"""
    title: str
    subtitle: Optional[str] = ""
    description: Optional[str] = ""
    cta_button_1: CTAButton = CTAButton()
    cta_button_2: CTAButton = CTAButton()
    background_type: Optional[str] = "slider"
    background_images: List[str] = []
    background_videos: List[str] = []
    overlay_opacity: Optional[float] = 0.4


# ===== 19. OFFERS & PROMOTIONS =====
class BannerConfig(BaseModel):
    """Banner configuration"""
    enabled: bool = False
    text: str = ""
    background_color: Optional[str] = ""
    text_color: Optional[str] = ""


class MidSection(BaseModel):
    """Mid-page promotional section"""
    enabled: bool = False
    type: str = "image"
    media_urls: List[str] = []


class PopupConfig(BaseModel):
    """Popup configuration"""
    enabled: bool = False
    title: str = ""
    description: Optional[str] = ""
    image: Optional[str] = ""
    cta_text: Optional[str] = "Get Offer"
    cta_link: Optional[str] = ""


class Popups(BaseModel):
    """Popup configurations"""
    entry: PopupConfig = PopupConfig()
    exit: PopupConfig = PopupConfig()
    idle: PopupConfig = PopupConfig()


class Offers(BaseModel):
    """Promotional offers configuration"""
    start_date: str = ""
    end_date: str = ""
    header: BannerConfig = BannerConfig()
    footer: BannerConfig = BannerConfig()
    mid_section: MidSection = MidSection()
    popups: Popups = Popups()


# ===== 20. SECTION ORDERING (OPTIONAL/HIDDEN) =====
class SectionOrder(BaseModel):
    """Individual section order entry"""
    section_name: str
    order: int = Field(ge=1)
    visible: bool = True


class SectionOrdering(BaseModel):
    """Section ordering configuration - OPTIONAL"""
    sections: List[SectionOrder] = []


# ============= MAIN LANDING PAGE SCHEMAS =============

class LandingPageBase(BaseModel):
    """
    Complete landing page structure with all sections
    
    FEATURES:
    - Why Choose Us section
    - Custom Sections (Format 1 & Format 2)
    - Updated custom trips with badge and itinerary
    - Section ordering is OPTIONAL
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
    why_choose_us: Optional[WhyChooseUs] = WhyChooseUs()
    attractions: Optional[Attractions] = Attractions()
    gallery: Optional[Gallery] = Gallery()
    testimonials: Optional[Testimonials] = Testimonials()
    faqs: Optional[FAQs] = FAQs()
    travel_guidelines: Optional[TravelGuidelines] = TravelGuidelines()
    
    # Custom sections
    custom_sections: Optional[CustomSections] = CustomSections()
    
    # Offers and promotions
    offers: Optional[Offers] = Offers()
    
    # Section ordering (OPTIONAL - hidden from basic UI)
    section_order: Optional[SectionOrdering] = None


class LandingPageCreate(LandingPageBase):
    """Schema for creating a landing page"""
    pass


class LandingPageUpdate(BaseModel):
    """Schema for updating a landing page"""
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
    why_choose_us: Optional[WhyChooseUs] = None
    attractions: Optional[Attractions] = None
    gallery: Optional[Gallery] = None
    testimonials: Optional[Testimonials] = None
    faqs: Optional[FAQs] = None
    travel_guidelines: Optional[TravelGuidelines] = None
    custom_sections: Optional[CustomSections] = None
    offers: Optional[Offers] = None
    section_order: Optional[SectionOrdering] = None


class LandingPageResponse(LandingPageBase):
    """Response schema for landing page"""
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
    """Landing page list item"""
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
    """Paginated landing pages response"""
    pages: List[LandingPageList]
    total: int
    page: int
    per_page: int
    total_pages: int


# Rebuild to resolve forward references
Packages.model_rebuild()