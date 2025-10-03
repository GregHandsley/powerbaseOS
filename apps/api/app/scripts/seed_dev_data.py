import asyncio
import datetime as dt
from sqlalchemy import select, func, text
from app.core.db import SessionLocal, engine
from app.models.facility import Facility
from app.models.side import Side
from app.models.rack import Rack
from app.models.timeslot import Timeslot

TZ = dt.timezone.utc  # adjust later based on facility.timezone if desired

async def seed():
    async with SessionLocal() as db:
        # Facility
        res = await db.execute(select(Facility).where(Facility.slug == "powerbase"))
        facility = res.scalar_one_or_none()
        if not facility:
            facility = Facility(name="Powerbase", slug="powerbase", timezone="Europe/London")
            db.add(facility); await db.flush()

        # Sides
        def ensure_side(code, name):
            return Side(facility_id=facility.id, code=code, name=name)

        res = await db.execute(select(Side).where(Side.facility_id == facility.id))
        existing = { (s.code): s for s in res.scalars().all() }
        power = existing.get("POWER") or ensure_side("POWER", "Power")
        base  = existing.get("BASE")  or ensure_side("BASE", "Base")
        if not power.id: db.add(power)
        if not base.id: db.add(base)
        await db.flush()

        # Racks (R1..R6 on both sides)
        for side in (power, base):
            res = await db.execute(select(Rack).where(Rack.side_id == side.id))
            have = { r.name for r in res.scalars().all() }
            for i in range(1, 7):
                name = f"R{i}"
                if name not in have:
                    db.add(Rack(side_id=side.id, name=name, is_active=True))

        # Timeslots: today every hour from 06:00–10:00
        today = dt.datetime.now(TZ).date()
        start_hour, end_hour = 6, 10
        for side in (power, base):
            for h in range(start_hour, end_hour):
                starts = dt.datetime.combine(today, dt.time(h, 0, tzinfo=TZ), tzinfo=TZ)
                ends   = starts + dt.timedelta(hours=1)
                exists = await db.execute(
                    select(Timeslot).where(
                        Timeslot.side_id==side.id,
                        Timeslot.starts_at==starts,
                        Timeslot.ends_at==ends
                    )
                )
                if not exists.scalars().first():
                    db.add(Timeslot(side_id=side.id, starts_at=starts, ends_at=ends, capacity=6))
        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed())
