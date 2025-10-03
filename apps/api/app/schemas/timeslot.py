from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TimeslotCreate(BaseModel):
    side_id: int
    starts_at: datetime
    ends_at: datetime
    capacity: int = 0

class TimeslotUpdate(BaseModel):
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    capacity: Optional[int] = None

class TimeslotRead(BaseModel):
    id: int
    side_id: int
    starts_at: datetime
    ends_at: datetime
    capacity: int
    class Config: from_attributes = True
