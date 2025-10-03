from __future__ import annotations
import datetime as dt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Integer, ForeignKey, UniqueConstraint
from . import Base

class Timeslot(Base):
    __tablename__ = "timeslots"
    __table_args__ = (UniqueConstraint("side_id", "starts_at", "ends_at", name="uq_timeslot_side_span"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    side_id: Mapped[int] = mapped_column(ForeignKey("sides.id", ondelete="CASCADE"), index=True)

    starts_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), index=True)
    ends_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), index=True)
    capacity: Mapped[int] = mapped_column(Integer, default=0)

    side = relationship("Side", back_populates="timeslots")
