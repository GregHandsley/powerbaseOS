from __future__ import annotations
import datetime as dt
from typing import Any, Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB

from . import Base, utcnow

class Job(Base):
    """
    Generic job tracking row for background work.
    """
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(120), index=True)           # e.g., "hold.expiry", "report.daily"
    status: Mapped[str] = mapped_column(String(32), index=True, default="pending")  # pending|running|succeeded|failed
    progress: Mapped[int] = mapped_column(Integer, default=0)            # 0..100

    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict) # input/args
    result:  Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict) # output/summary

    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, index=True)