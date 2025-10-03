from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rack import Rack

async def list_racks(db: AsyncSession, side_id: int | None = None):
    stmt = select(Rack)
    if side_id is not None:
        stmt = stmt.where(Rack.side_id == side_id)
    res = await db.execute(stmt.order_by(Rack.name))
    return res.scalars().all()

async def get_rack(db: AsyncSession, rack_id: int):
    return await db.get(Rack, rack_id)

async def create_rack(db: AsyncSession, data: dict):
    obj = Rack(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def update_rack(db: AsyncSession, rack_id: int, data: dict):
    obj = await db.get(Rack, rack_id)
    if not obj: return None
    for k, v in data.items():
        if v is not None: setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_rack(db: AsyncSession, rack_id: int) -> bool:
    obj = await db.get(Rack, rack_id)
    if not obj: return False
    await db.delete(obj)
    await db.commit()
    return True
