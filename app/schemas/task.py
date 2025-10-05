# app/schemas/task.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    priority: str
    description: Optional[str]
    assigned_to: int
    due_date: date
    status: Optional[str] = "Pending"
    tenant_id: int

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True