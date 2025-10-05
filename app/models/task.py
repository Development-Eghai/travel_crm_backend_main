# app/models/task.py
from sqlalchemy import Column, Integer, String, Text, Date, Enum, ForeignKey, DateTime
from datetime import datetime
from core.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    priority = Column(Enum("Low", "Medium", "High", name="task_priority_enum"), nullable=False)
    description = Column(Text, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(Enum("Pending", "Completed", name="task_status_enum"), default="Pending", nullable=False)
    tenant_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())