from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_value = Column(String(255), unique=True, nullable=False)
    label = Column(String(100))
    tenant_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    revoked_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="api_keys")