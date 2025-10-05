from core.database import Base
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=True)

    client_name = Column(String)
    client_email = Column(String)
    client_phone = Column(String)
    client_gst = Column(String)
    client_address = Column(Text)

    invoice_number = Column(String, unique=True)
    invoice_date = Column(Date, default=date.today)
    due_date = Column(Date)
    is_interstate = Column(Boolean, default=False)

    subtotal = Column(Float)
    discount = Column(Float)
    taxable_amount = Column(Float)
    cgst = Column(Float)
    sgst = Column(Float)
    igst = Column(Float)
    total_amount = Column(Float)
    due_amount = Column(Float)

    template = Column(String)

    terms_and_conditions = Column(Text)
    payment_terms = Column(Text)
    cancellation_policy = Column(Text)
    notes = Column(Text)

    items = relationship("InvoiceItem", backref="invoice", cascade="all, delete")
    payments = relationship("InvoicePayment", backref="invoice", cascade="all, delete")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    item_name = Column(String)
    description = Column(Text)
    hsn_code = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    discount = Column(Float)
    discount_type = Column(String)  # "amount" or "percent"
    gst_percent = Column(Float)


class InvoicePayment(Base):
    __tablename__ = "invoice_payments"
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    amount = Column(Float)
    method = Column(String)
    date = Column(Date)
    transaction_id = Column(String)
    notes = Column(Text)