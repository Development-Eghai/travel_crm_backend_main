from core.database import Base
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    # NEW SAFE MIGRATION FIELD
    lead_id = Column(Integer, unique=True, index=True, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

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
    status = Column(String, default="New")
    priority = Column(String, default="Medium")
    assigned_to = Column(Integer, ForeignKey("users.id"))
    follow_up_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now())
    source = Column(String)

    is_deleted = Column(Boolean, default=False)

    comments = relationship("LeadComment", backref="lead", cascade="all, delete")
    documents = relationship("LeadDocument", backref="lead", cascade="all, delete")
