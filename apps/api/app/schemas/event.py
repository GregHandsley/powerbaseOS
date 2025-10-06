from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict

class EventRead(BaseModel):
    id: int
    type: str
    payload_json: Dict[str, Any]
    created_at: datetime
    class Config:
        from_attributes = True