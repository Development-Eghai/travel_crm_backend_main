# app/models/lead_assignment.py
from sqlalchemy import Column, Integer, Text, Date, Enum, ForeignKey, DateTime
from datetime import datetime
from core.database import Base

class LeadAssignment(Base):
    __tablename__ = "lead_assignments"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=False)
    due_date = Column(Date, nullable=False)
    priority = Column(Enum("Low", "Medium", "High", name="priority_enum"), nullable=False)
    follow_up_date = Column(Date, nullable=False)
    comments = Column(Text, nullable=True)
    tenant_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())