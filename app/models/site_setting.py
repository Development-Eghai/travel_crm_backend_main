from core.database import Base
from sqlalchemy import Column, Integer, String, Text

class GlobalSettings(Base):
    __tablename__ = "global_settings"
    id = Column(Integer, primary_key=True)

    # General
    site_title = Column(String)
    tagline = Column(String)
    company_name = Column(String)
    site_description = Column(Text)
    logo_url = Column(String)
    favicon_url = Column(String)
    homepage_slider = Column(Text)  # comma-separated URLs

    # Contact
    contact_email = Column(String)
    contact_phones = Column(Text)  # comma-separated
    business_address = Column(Text)
    social_links = Column(Text)  # comma-separated
    google_map_link = Column(String)

    # Payment
    bank_name = Column(String)
    account_number = Column(String)
    ifsc_code = Column(String)
    branch_name = Column(String)
    upi_ids = Column(Text)  # comma-separated
    qr_code_images = Column(Text)  # comma-separated
    quotation_format = Column(String)
    invoice_format = Column(String)

    # Menu
    header_menu = Column(Text)
    footer_menu = Column(Text)

    # SEO
    meta_title = Column(String)
    meta_description = Column(Text)
    meta_tags = Column(Text)  # comma-separated
    og_title = Column(String)
    og_description = Column(Text)
    og_image = Column(String)

    # Policies
    terms_conditions = Column(Text)
    privacy_policy = Column(Text)
    payment_terms = Column(Text)
    cancellation_policy = Column(Text)
    refund_policy = Column(Text)

    # Email Templates
    email_incoming = Column(Text)
    email_form_submitted = Column(Text)
    email_quotation_sent = Column(Text)
    email_invoice_sent = Column(Text)
    email_lead_assigned = Column(Text)
    email_payment_confirmation = Column(Text)
    email_invoice_due = Column(Text)
    email_trip_updates = Column(Text)
    email_follow_up = Column(Text)