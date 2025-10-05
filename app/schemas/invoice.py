from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class InvoiceItemIn(BaseModel):
    item_name: str
    description: Optional[str]
    hsn_code: Optional[str]
    quantity: int
    unit_price: float
    discount: Optional[float] = 0.0
    discount_type: Optional[str] = "amount"
    gst_percent: float

class InvoiceTerms(BaseModel):
    terms_and_conditions: Optional[str]
    payment_terms: Optional[str]
    cancellation_policy: Optional[str]
    notes: Optional[str]

class InvoicePaymentIn(BaseModel):
    amount: float
    method: str
    date: date
    transaction_id: Optional[str]
    notes: Optional[str]

class InvoiceCreate(BaseModel):
    lead_id: int
    quotation_id: Optional[int]
    client_name: str
    client_email: str
    client_phone: str
    client_gst: Optional[str]
    client_address: Optional[str]

    invoice_number: Optional[str]
    invoice_date: date
    due_date: date
    is_interstate: bool

    items: List[InvoiceItemIn]
    terms: InvoiceTerms
    template: Optional[str] = "Default"
    payment: Optional[InvoicePaymentIn]