from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.timeslot import TimeslotCreate, TimeslotRead, TimeslotUpdate
from app.services.timeslots import list_timeslots, get_timeslot, create_timeslot, update_timeslot, delete_timeslot

router = APIRouter(prefix="/timeslots", tags=["timeslots"])

@router.get("/", response_model=list[TimeslotRead])
async def list_(side_id: int | None = Query(None), db: AsyncSession = Depends(get_db)):
    return await list_timeslots(db, side_id)

@router.get("/{timeslot_id}", response_model=TimeslotRead)
async def get_(timeslot_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_timeslot(db, timeslot_id)
    if not obj: raise HTTPException(404, "Timeslot not found")
    return obj

@router.post("/", response_model=TimeslotRead, status_code=201)
async def create_(payload: TimeslotCreate, db: AsyncSession = Depends(get_db)):
    return await create_timeslot(db, payload.model_dump())

@router.patch("/{timeslot_id}", response_model=TimeslotRead)
async def update_(timeslot_id: int, payload: TimeslotUpdate, db: AsyncSession = Depends(get_db)):
    obj = await update_timeslot(db, timeslot_id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(404, "Timeslot not found")
    return obj

@router.delete("/{timeslot_id}", status_code=204)
async def delete_(timeslot_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_timeslot(db, timeslot_id)
    if not ok: raise HTTPException(404, "Timeslot not found")
