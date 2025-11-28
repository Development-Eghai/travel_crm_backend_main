from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date as date_type, datetime

# ------------------------------
# AGENT
# ------------------------------
class AgentInfo(BaseModel):
    name: str
    email: str
    contact: str


# ------------------------------
# COMPANY
# ------------------------------
class CompanyInfo(BaseModel):
    name: str
    email: str
    mobile: str
    website: Optional[str] = "" 
    licence: Optional[str] = ""
    logo_url: Optional[str] = ""


# ------------------------------
# TRIP DETAILS
# ------------------------------
class TripSection(BaseModel):
    title: str
    content: str


class TripDetails(BaseModel):
    trip_id: Optional[int] = None 
    display_title: str
    overview: str
    hero_image: Optional[str] = ""
    gallery_images: List[str] = []
    sections: List[TripSection] = []
    
    @field_validator('gallery_images', mode='before')
    def filter_empty_gallery_images(cls, v):
        """Remove empty strings from gallery_images"""
        if isinstance(v, list):
            return [url.strip() for url in v if url and url.strip()]
        return v or []


# ------------------------------
# ITINERARY
# ------------------------------
class ItineraryItem(BaseModel):
    day: int
    title: str
    description: str


# ------------------------------
# COSTING - FULL PACKAGE SUPPORT + ITEMS WITH IMAGES
# ------------------------------
class CostingItem(BaseModel):
    """Simple item for itemized costing - NOW WITH IMAGES"""
    name: str
    description: Optional[str] = "" 
    quantity: int = 1 
    unit_price: int = 0
    image_urls: List[str] = []  # Multiple images for items
    
    @field_validator('image_urls', mode='before')
    def filter_empty_image_urls(cls, v):
        """Remove empty strings from image_urls"""
        if isinstance(v, list):
            return [url.strip() for url in v if url and url.strip()]
        return v or []


class ComponentVariant(BaseModel):
    """Individual option within a component"""
    title: str = ""
    description: str = ""
    image_urls: List[str] = []  # Multiple images support
    price_per_person: int = 0
    is_selected: bool = False
    
    @field_validator('image_urls', mode='before')
    def filter_empty_image_urls(cls, v):
        """Remove empty strings from image_urls"""
        if isinstance(v, list):
            return [url.strip() for url in v if url and url.strip()]
        return v or []


class PackageComponent(BaseModel):
    """A component of the package (e.g., Hotels, Transport)"""
    component_type: str
    component_title: str
    variants: List[ComponentVariant]


class PackageOption(BaseModel):
    """Complete package option"""
    package_id: str
    package_name: str
    package_description: str = ""
    is_active: bool = True
    components: List[PackageComponent] = []
    total_price: int = 0


class Costing(BaseModel):
    """Costing structure - supports BOTH package-based and simple items"""
    type: str  # "person" or "package"
    currency: Optional[str] = "INR"
    total_amount: int
    selected_package_id: Optional[str] = None
    
    # Package-based pricing
    packages: List[PackageOption] = []
    
    # Simple items (WITH IMAGES)
    items: List[CostingItem] = []


# ------------------------------
# POLICIES
# ------------------------------
class Policies(BaseModel):
    payment_terms: str = ""
    cancellation_policy: str = ""
    terms_and_conditions: str = ""
    custom_policy: Optional[str] = ""


# ------------------------------
# PAYMENT
# ------------------------------
class PaymentDetails(BaseModel):
    bank_name: str = ""
    account_number: str = ""
    ifsc_code: str = ""
    branch_name: str = ""
    gst_number: Optional[str] = ""
    address: Optional[str] = ""
    upi_ids: List[str] = []
    qr_code_url: Optional[str] = ""


# ------------------------------
# CREATE SCHEMA
# ------------------------------
class QuotationCreate(BaseModel):
    lead_id: int = 0
    design: str
    agent: AgentInfo
    company: CompanyInfo
    trip: TripDetails
    itinerary: List[ItineraryItem]
    costing: Costing
    policies: Policies
    payment: PaymentDetails
    status: Optional[str] = "Draft"
    amount: Optional[int] = 0
    date: Optional[date_type] = None  # Use date_type instead of string
    
    # Client fields stored directly on the main Quotation table
    client_name: Optional[str] = "" 
    client_email: Optional[str] = ""
    client_mobile: Optional[str] = ""

    @field_validator('date', mode='before')
    def parse_date(cls, v):
        """Parse date string to date object or use today if None"""
        if v is None:
            return date_type.today()
        if isinstance(v, date_type):
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                return date_type.today()
        return date_type.today()


# ------------------------------
# UPDATE SCHEMA (Partial update)
# ------------------------------
class QuotationUpdate(BaseModel):
    design: Optional[str] = None
    status: Optional[str] = None
    amount: Optional[int] = None
    date: Optional[date_type] = None  # Use date_type instead of string

    agent: Optional[AgentInfo] = None
    company: Optional[CompanyInfo] = None
    trip: Optional[TripDetails] = None
    itinerary: Optional[List[ItineraryItem]] = None
    costing: Optional[Costing] = None
    policies: Optional[Policies] = None
    payment: Optional[PaymentDetails] = None
    
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_mobile: Optional[str] = None

    @field_validator('date', mode='before')
    def parse_date(cls, v):
        """Parse date string to date object"""
        if v is None:
            return None
        if isinstance(v, date_type):
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                return None
        return None


# ------------------------------
# OUTPUT SCHEMA
# ------------------------------
class QuotationOut(BaseModel):
    id: int
    lead_id: int
    design: str
    status: str
    amount: Optional[int]
    date: date_type
    client_name: Optional[str] = ""
    client_email: Optional[str] = ""
    client_mobile: Optional[str] = ""
    hero_image: Optional[str] = ""
    gallery_images: Optional[List[str]] = []

    class Config:
        from_attributes = True