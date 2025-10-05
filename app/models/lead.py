from core.database import Base
from sqlalchemy import Column, Integer, String, Text, Date, Time, Enum, ForeignKey, DateTime
from sqlalchemy import Column, Integer, String, Text, Date, Time, Enum, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

# models/lead.py
class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    destination_type = Column(String, nullable=False)
    pickup = Column(String)
    drop = Column(String)
    travel_from = Column(Date)
    travel_to = Column(Date)
    adults = Column(Integer)
    children = Column(Integer)
    status = Column(String, default="New")  # New, Contacted, Quotation Sent, etc.
    priority = Column(String, default="Medium")  # Low, Medium, High
    assigned_to = Column(Integer, ForeignKey("users.id"))
    follow_up_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now())
    source = Column(String)

    comments = relationship("LeadComment", backref="lead", cascade="all, delete")
    documents = relationship("LeadDocument", backref="lead", cascade="all, delete")