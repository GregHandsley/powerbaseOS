from __future__ import annotations
import datetime as dt
from typing import Any

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from . import Base, utcnow

class Event(Base):
    """
    Immutable append-only activity log.
    """
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(120), index=True)  # e.g., "timeslot.created"
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)