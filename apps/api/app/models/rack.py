from __future__ import annotations
import datetime as dt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, DateTime, UniqueConstraint
from . import Base, utcnow

class Rack(Base):
    __tablename__ = "racks"
    __table_args__ = (UniqueConstraint("side_id", "name", name="uq_rack_side_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    side_id: Mapped[int] = mapped_column(ForeignKey("sides.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    side = relationship("Side", back_populates="racks")
