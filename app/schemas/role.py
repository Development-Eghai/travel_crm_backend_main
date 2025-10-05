# app/schemas/role.py
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class RoleBase(BaseModel):
    name: str
    modules: Optional[Dict[str, bool]] = {}
    tenant_id: int

class RoleCreate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True