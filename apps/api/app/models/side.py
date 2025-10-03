from __future__ import annotations
import datetime as dt
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, UniqueConstraint
from . import Base, utcnow

class Side(Base):
    __tablename__ = "sides"
    __table_args__ = (UniqueConstraint("facility_id", "code", name="uq_side_facility_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    code: Mapped[str] = mapped_column(String(50))

    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    facility: Mapped["Facility"] = relationship(back_populates="sides")
    racks: Mapped[List["Rack"]] = relationship(back_populates="side", cascade="all, delete-orphan")
    timeslots: Mapped[List["Timeslot"]] = relationship(back_populates="side", cascade="all, delete-orphan")
