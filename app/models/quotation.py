# models/quotation.py
from core.database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Quotation(Base):
    __tablename__ = "quotations"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    design = Column(String, nullable=False)
    status = Column(String, default="Draft")
    amount = Column(Integer)
    date = Column(Date, default=datetime.utcnow)

    agent = relationship("QuotationAgent", backref="quotation", uselist=False, cascade="all, delete")
    company = relationship("QuotationCompany", backref="quotation", uselist=False, cascade="all, delete")
    trip = relationship("QuotationTrip", backref="quotation", uselist=False, cascade="all, delete")
    itinerary = relationship("QuotationItinerary", backref="quotation", cascade="all, delete")
    costing = relationship("QuotationCosting", backref="quotation", uselist=False, cascade="all, delete")
    policies = relationship("QuotationPolicies", backref="quotation", uselist=False, cascade="all, delete")
    payment = relationship("QuotationPayment", backref="quotation", uselist=False, cascade="all, delete")

class QuotationAgent(Base):
    __tablename__ = "quotation_agents"
    id = Column(Integer, primary_key=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"))
    name = Column(String)
    email = Column(String)
    contact = Column(String)

class QuotationCompany(Base):
    __tablename__ = "quotation_companies"
    id = Column(Integer, primary_key=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"))
    name = Column(String)
    email = Column(String)
    mobile = Column(String)
    website = Column(String)
    licence = Column(String)
    logo_url = Column(String)

class QuotationTrip(Base):
    __tablename__ = "quotation_trips"
    id = Column(Integer, primary_key=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"))
    display_title = Column(String)
    overview = Column(Text)
    hero_image = Column(String)
    gallery_images = Column(Text)  # comma-separated URLs

class QuotationTripSection(Base):
    __tablename__ = "quotation_trip_sections"
    id = Column(Integer, primary_key=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"))
    title = Column(String)
    content = Column(Text)

class QuotationItinerary(Base):
    __tablename__ = "quotation_itinerary"
    id = Column(Integer, primary_key=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"))
    day = Column(Integer)
    title = Column(String)
    description = Column(Text)

class QuotationCosting(Base):
    __tablename__ = "quotation_costing"
    id = Column(Integer, primary_key=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"))
    type = Column(String)  # customised / fixed
    price_per_person = Column(Integer)
    price_per_package = Column(Integer)
    selected_slot = Column(String)
    selected_package = Column(String)

class QuotationPolicies(Base):
    __tablename__ = "quotation_policies"
    id = Column(Integer, primary_key=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"))
    payment_terms = Column(Text)
    cancellation_policy = Column(Text)
    terms_and_conditions = Column(Text)
    custom_policy = Column(Text)

class QuotationPayment(Base):
    __tablename__ = "quotation_payment"
    id = Column(Integer, primary_key=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"))
    bank_name = Column(String)
    account_number = Column(String)
    ifsc_code = Column(String)
    branch_name = Column(String)
    gst_number = Column(String)
    address = Column(Text)
    upi_ids = Column(Text)  # comma-separated
    qr_code_url = Column(String)