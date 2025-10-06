from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.event import Event

async def log_event(db: AsyncSession, type_: str, payload: Dict[str, Any]) -> Event:
    e = Event(type=type_, payload_json=payload)
    db.add(e)
    # Caller controls transaction; we don't commit here to allow atomicity with the action that triggered it.
    return e

async def list_events(db: AsyncSession, limit: int = 50) -> List[Event]:
    stmt = select(Event).order_by(desc(Event.created_at)).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()