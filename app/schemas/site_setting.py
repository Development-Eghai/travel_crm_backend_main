from pydantic import BaseModel
from typing import Optional, List

class GlobalSettingsSchema(BaseModel):
    site_title: Optional[str]
    tagline: Optional[str]
    company_name: Optional[str]
    site_description: Optional[str]
    logo_url: Optional[str]
    favicon_url: Optional[str]
    homepage_slider: Optional[List[str]]

    contact_email: Optional[str]
    contact_phones: Optional[List[str]]
    business_address: Optional[str]
    social_links: Optional[List[str]]
    google_map_link: Optional[str]

    bank_name: Optional[str]
    account_number: Optional[str]
    ifsc_code: Optional[str]
    branch_name: Optional[str]
    upi_ids: Optional[List[str]]
    qr_code_images: Optional[List[str]]
    quotation_format: Optional[str]
    invoice_format: Optional[str]

    header_menu: Optional[str]
    footer_menu: Optional[str]

    meta_title: Optional[str]
    meta_description: Optional[str]
    meta_tags: Optional[List[str]]
    og_title: Optional[str]
    og_description: Optional[str]
    og_image: Optional[str]

    terms_conditions: Optional[str]
    privacy_policy: Optional[str]
    payment_terms: Optional[str]
    cancellation_policy: Optional[str]
    refund_policy: Optional[str]

    email_incoming: Optional[str]
    email_form_submitted: Optional[str]
    email_quotation_sent: Optional[str]
    email_invoice_sent: Optional[str]
    email_lead_assigned: Optional[str]
    email_payment_confirmation: Optional[str]
    email_invoice_due: Optional[str]
    email_trip_updates: Optional[str]
    email_follow_up: Optional[str]