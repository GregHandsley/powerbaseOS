from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Auth payloads
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

# Users
class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    roles: List[str] = []
    class Config:
        from_attributes = True

# (Optional) for admin create/update in future sprints
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = ""
    password: str
    roles: List[str] = []

class RefreshRequest(BaseModel):
    token: str