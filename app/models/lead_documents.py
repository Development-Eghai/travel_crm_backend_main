from core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

class LeadDocument(Base):
    __tablename__ = "lead_documents"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # e.g. /uploads/leads/filename.pdf
    uploaded_by = Column(Integer, ForeignKey("users.id"))  # optional: who uploaded
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Optional relationships
    uploader = relationship("User", backref="uploaded_documents", lazy="joined")