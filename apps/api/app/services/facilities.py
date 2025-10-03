from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.facility import Facility

async def list_facilities(db: AsyncSession):
    res = await db.execute(select(Facility).order_by(Facility.name))
    return res.scalars().all()

async def get_facility(db: AsyncSession, facility_id: int):
    return await db.get(Facility, facility_id)

async def create_facility(db: AsyncSession, data: dict):
    obj = Facility(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def update_facility(db: AsyncSession, facility_id: int, data: dict):
    obj = await db.get(Facility, facility_id)
    if not obj: return None
    for k, v in data.items():
        if v is not None: setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_facility(db: AsyncSession, facility_id: int) -> bool:
    obj = await db.get(Facility, facility_id)
    if not obj: return False
    await db.delete(obj)
    await db.commit()
    return True
