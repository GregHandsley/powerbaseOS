from pydantic import BaseModel
from typing import Optional

class SideCreate(BaseModel):
    facility_id: int
    name: str
    code: str

class SideUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None

class SideRead(BaseModel):
    id: int
    facility_id: int
    name: str
    code: str
    class Config: from_attributes = True
