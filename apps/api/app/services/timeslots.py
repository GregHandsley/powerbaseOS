from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.timeslot import Timeslot
from app.services.events import log_event

async def list_timeslots(db: AsyncSession, side_id: int | None = None):
    stmt = select(Timeslot)
    if side_id is not None:
        stmt = stmt.where(Timeslot.side_id == side_id)
    res = await db.execute(stmt.order_by(Timeslot.starts_at))
    return res.scalars().all()

async def get_timeslot(db: AsyncSession, timeslot_id: int):
    return await db.get(Timeslot, timeslot_id)

async def create_timeslot(db: AsyncSession, data: dict):
    obj = Timeslot(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def update_timeslot(db: AsyncSession, timeslot_id: int, data: dict):
    obj = await db.get(Timeslot, timeslot_id)
    if not obj: return None
    for k, v in data.items():
        if v is not None: setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_timeslot(db: AsyncSession, timeslot_id: int) -> bool:
    obj = await db.get(Timeslot, timeslot_id)
    if not obj: return False
    await db.delete(obj)
    await db.commit()
    return True

async def create_timeslot(db: AsyncSession, data: dict):
    obj = Timeslot(**data)
    db.add(obj)
    await db.flush()  # assign obj.id before logging

    await log_event(
        db,
        "timeslot.created",
        {
            "timeslot_id": obj.id,
            "side_id": obj.side_id,
            "starts_at": obj.starts_at.isoformat() if obj.starts_at else None,
            "ends_at": obj.ends_at.isoformat() if obj.ends_at else None,
            "capacity": obj.capacity,
        },
    )

    await db.commit()
    await db.refresh(obj)
    return obj