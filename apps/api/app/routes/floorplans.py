from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.services.floorplans import create_draft, get_by_id, update_scene, publish, get_latest_published

router = APIRouter(prefix="/floorplans", tags=["floorplans"])

@router.post("/draft", status_code=201)
async def create_draft_route(
    facility_id: int = Query(..., ge=1),
    db: AsyncSession = Depends(get_db),
):
    fp = await create_draft(db, facility_id, scene=None)
    return {"id": fp.id, "facility_id": fp.facility_id, "status": fp.status, "version": fp.version, "scene_json": fp.scene_json}

@router.patch("/{floorplan_id}/scene", status_code=200)
async def update_scene_route(
    floorplan_id: int,
    body: dict,
    db: AsyncSession = Depends(get_db),
):
    fp = await update_scene(db, floorplan_id, scene=body)
    if not fp:
        raise HTTPException(400, "Only draft floorplans can be edited or floorplan not found")
    return {"id": fp.id, "status": fp.status, "version": fp.version, "scene_json": fp.scene_json}

@router.post("/{floorplan_id}/publish", status_code=201)
async def publish_route(
    floorplan_id: int,
    db: AsyncSession = Depends(get_db),
):
    pub = await publish(db, floorplan_id)
    if not pub:
        raise HTTPException(400, "Cannot publish (missing draft?)")
    return {"id": pub.id, "status": pub.status, "version": pub.version}

# Kiosk: fetch latest published
@router.get("/kiosk/latest", status_code=200)
async def kiosk_latest_route(
    facility_id: int = Query(..., ge=1),
    db: AsyncSession = Depends(get_db),
):
    pub = await get_latest_published(db, facility_id)
    if not pub:
        return {"facility_id": facility_id, "status": "none", "scene_json": {"nodes": []}}
    return {"facility_id": pub.facility_id, "status": "published", "version": pub.version, "scene_json": pub.scene_json}