from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.floorplan import Floorplan, FloorplanStatus

async def create_draft(db: AsyncSession, facility_id: int, scene: Dict[str, Any] | None = None) -> Floorplan:
    # create a new draft (does not affect published)
    fp = Floorplan(facility_id=facility_id, status=FloorplanStatus.draft.value, scene_json=scene or {"nodes": []})
    db.add(fp)
    await db.commit(); await db.refresh(fp)
    return fp

async def get_latest_published(db: AsyncSession, facility_id: int) -> Optional[Floorplan]:
    stmt = select(Floorplan).where(
        Floorplan.facility_id == facility_id,
        Floorplan.status == FloorplanStatus.published.value
    ).order_by(desc(Floorplan.version), desc(Floorplan.id)).limit(1)
    res = await db.execute(stmt)
    return res.scalar_one_or_none()

async def get_by_id(db: AsyncSession, floorplan_id: int) -> Optional[Floorplan]:
    return await db.get(Floorplan, floorplan_id)

async def update_scene(db: AsyncSession, floorplan_id: int, scene: Dict[str, Any]) -> Optional[Floorplan]:
    fp = await db.get(Floorplan, floorplan_id)
    if not fp or fp.status != FloorplanStatus.draft.value:
        return None
    fp.scene_json = scene
    await db.commit(); await db.refresh(fp)
    return fp

async def publish(db: AsyncSession, floorplan_id: int) -> Optional[Floorplan]:
    # Publishing: clone draft into a new published revision OR convert the draft?
    # Sensible default: create a NEW published row with version = (latest_published_version+1)
    draft = await db.get(Floorplan, floorplan_id)
    if not draft or draft.status != FloorplanStatus.draft.value:
        return None

    # find latest published version
    latest = await get_latest_published(db, draft.facility_id)
    next_version = (latest.version + 1) if latest else 1

    pub = Floorplan(
        facility_id=draft.facility_id,
        status=FloorplanStatus.published.value,
        version=next_version,
        scene_json=draft.scene_json
    )
    db.add(pub)
    await db.commit(); await db.refresh(pub)
    return pub