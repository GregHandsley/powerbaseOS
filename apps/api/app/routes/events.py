from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.event import EventRead
from app.services.events import list_events

router = APIRouter(prefix="/events", tags=["events"])

@router.get("", response_model=list[EventRead])
async def recent_events(
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    return await list_events(db, limit=limit)