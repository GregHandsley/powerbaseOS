from pydantic import BaseModel
from typing import Optional

class RackCreate(BaseModel):
    side_id: int
    name: str
    is_active: bool = True

class RackUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class RackRead(BaseModel):
    id: int
    side_id: int
    name: str
    is_active: bool
    class Config: from_attributes = True
