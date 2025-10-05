from pydantic import BaseModel, EmailStr, constr
from enum import Enum
from datetime import datetime
from typing import Optional

class UserStatus(str, Enum):
    Active = "Active"
    Inactive = "Inactive"
    Suspended = "Suspended"
# 🎭 Enums
class UserRole(str, Enum):
    Admin = "Admin"
    Editor = "Editor"
    Agent = "Agent"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 🧱 Base User Schema
class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_number: Optional[str] = None
    role: UserRole
    send_user_email: bool = False
    website: Optional[str] = None
    tenant_id: int

# 🔐 User Creation Schema
class UserCreate(UserBase):
    password: constr(max_length=72) # type: ignore


# 🧾 API Key Schema
class APIKeyOut(BaseModel):
    id: int
    key_value: str
    label: Optional[str]
    tenant_id: int
    user_id: int
    is_active: bool
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}

# 🧑‍💼 User Output Schema
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_number: Optional[str] = None
    role: UserRole
    status: UserStatus  # ✅ added
    send_user_email: bool
    website: Optional[str] = None
    tenant_id: int

    model_config = {"from_attributes": True}

# 🔗 Composite Response
class UserWithKey(BaseModel):
    user: UserOut
    api_key: APIKeyOut