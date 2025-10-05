# schemas/quotation.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class AgentInfo(BaseModel):
    name: str
    email: str
    contact: str

class CompanyInfo(BaseModel):
    name: str
    email: str
    mobile: str
    website: Optional[str]
    licence: Optional[str]
    logo_url: Optional[str]

class TripSection(BaseModel):
    title: str
    content: str

class TripDetails(BaseModel):
    display_title: str
    overview: str
    hero_image: Optional[str]
    gallery_images: List[str]
    sections: List[TripSection]

class ItineraryItem(BaseModel):
    day: int
    title: str
    description: str

class Costing(BaseModel):
    type: str
    price_per_person: Optional[int]
    price_per_package: Optional[int]
    selected_slot: Optional[str]
    selected_package: Optional[str]

class Policies(BaseModel):
    payment_terms: str
    cancellation_policy: str
    terms_and_conditions: str
    custom_policy: Optional[str]

class PaymentDetails(BaseModel):
    bank_name: str
    account_number: str
    ifsc_code: str
    branch_name: str
    gst_number: Optional[str]
    address: Optional[str]
    upi_ids: List[str]
    qr_code_url: Optional[str]

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

class QuotationOut(BaseModel):
    id: int
    lead_id: int
    design: str
    status: str
    amount: int
    date: date

    class Config:
        from_attributes = True
