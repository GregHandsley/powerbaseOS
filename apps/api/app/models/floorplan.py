from __future__ import annotations
import datetime as dt
import enum
from typing import Any, Dict

from sqlalchemy import String, DateTime, Integer, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from . import Base, utcnow

class FloorplanStatus(str, enum.Enum):
    draft = "draft"
    published = "published"

class Floorplan(Base):
    __tablename__ = "floorplans"

    id: Mapped[int] = mapped_column(primary_key=True)
    facility_id: Mapped[int] = mapped_column(Integer, index=True)
    status: Mapped[str] = mapped_column(Enum(FloorplanStatus), index=True, default=FloorplanStatus.draft.value)
    version: Mapped[int] = mapped_column(Integer, default=1)
    scene_json: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)

    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)