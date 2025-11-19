from pydantic import BaseModel
from typing import Optional, List
from datetime import date

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
    website: Optional[str]
    licence: Optional[str]
    logo_url: Optional[str]


# ------------------------------
# TRIP DETAILS
# ------------------------------
class TripSection(BaseModel):
    title: str
    content: str


class TripDetails(BaseModel):
    display_title: str
    overview: str
    hero_image: Optional[str]
    gallery_images: List[str]
    sections: List[TripSection]


# ------------------------------
# ITINERARY
# ------------------------------
class ItineraryItem(BaseModel):
    day: int
    title: str
    description: str


# ------------------------------
# COSTING (UPDATED)
# ------------------------------
class CostingItem(BaseModel):
    name: str
    quantity: int
    unit_price: int


class Costing(BaseModel):
    type: str
    currency: Optional[str] = "INR"
    total_amount: int
    items: List[CostingItem]


# ------------------------------
# POLICIES
# ------------------------------
class Policies(BaseModel):
    payment_terms: str
    cancellation_policy: str
    terms_and_conditions: str
    custom_policy: Optional[str]


# ------------------------------
# PAYMENT
# ------------------------------
class PaymentDetails(BaseModel):
    bank_name: str
    account_number: str
    ifsc_code: str
    branch_name: str
    gst_number: Optional[str]
    address: Optional[str]
    upi_ids: List[str]
    qr_code_url: Optional[str]


# ------------------------------
# CREATE SCHEMA
# ------------------------------
class QuotationCreate(BaseModel):
    lead_id: int
    design: str
    agent: AgentInfo
    company: CompanyInfo
    trip: TripDetails
    itinerary: List[ItineraryItem]
    costing: Costing
    policies: Policies
    payment: PaymentDetails
    status: Optional[str] = "Draft"
    amount: Optional[int]
    date: Optional[date]


# ------------------------------
# UPDATE SCHEMA (Partial update)
# ------------------------------
class QuotationUpdate(BaseModel):
    design: Optional[str]
    status: Optional[str]
    amount: Optional[int]
    date: Optional[date]

    agent: Optional[AgentInfo]
    company: Optional[CompanyInfo]
    trip: Optional[TripDetails]
    itinerary: Optional[List[ItineraryItem]]
    costing: Optional[Costing]
    policies: Optional[Policies]
    payment: Optional[PaymentDetails]


# ------------------------------
# SMALL LIST OUTPUT SCHEMA
# ------------------------------
class QuotationOut(BaseModel):
    id: int
    lead_id: int
    design: str
    status: str
    amount: Optional[int]
    date: date

    class Config:
        from_attributes = True