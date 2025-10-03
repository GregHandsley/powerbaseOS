from pydantic import BaseModel, Field
from typing import Optional

class FacilityCreate(BaseModel):
    name: str
    slug: str
    timezone: str = "Europe/London"

class FacilityUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    timezone: Optional[str] = None

class FacilityRead(BaseModel):
    id: int
    name: str
    slug: str
    timezone: str
    class Config: from_attributes = True
