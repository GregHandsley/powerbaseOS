from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from datetime import datetime, timezone

from app.core.db import get_db
from app.models.rack import Rack
from sqlalchemy import select
from app.models.side import Side

router = APIRouter(prefix="/kiosk", tags=["kiosk"])

def parse_at(at: str | None) -> datetime:
    if not at:
        return datetime.now(timezone.utc)
    try:
        return datetime.fromisoformat(at.replace("Z", "+00:00"))
    except Exception:
        raise HTTPException(400, "Invalid 'at' timestamp")

@router.get("/availability")
async def kiosk_availability(
    facility_id: int = Query(..., ge=1),
    at: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    ts = parse_at(at)

    # Racks in facility (via Side → Facility)
    stmt = (
        select(Rack.id, Rack.name)
        .select_from(Rack.__table__.join(Side.__table__, Rack.side_id == Side.id))
        .where(Side.facility_id == facility_id)
    )
    racks = (await db.execute(stmt)).mappings().all()

    rack_ids = [r["id"] for r in racks]
    if not rack_ids:
        return {"facility_id": facility_id, "at": ts.isoformat(), "racks": []}

    status_by_rack = {rid: {"status": "available"} for rid in rack_ids}

    return {
        "facility_id": facility_id,
        "at": ts.isoformat(),
        "racks": [
            {
                "rack_id": r["id"],
                "name": r["name"],
                **status_by_rack.get(r["id"], {"status": "available"}),
            }
            for r in racks
        ],
    }