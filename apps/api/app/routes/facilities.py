from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.facility import FacilityCreate, FacilityRead, FacilityUpdate
from app.services.facilities import list_facilities, get_facility, create_facility, update_facility, delete_facility

router = APIRouter(prefix="/facilities", tags=["facilities"])

@router.get("/", response_model=list[FacilityRead])
async def list_(db: AsyncSession = Depends(get_db)):
    return await list_facilities(db)

@router.get("/{facility_id}", response_model=FacilityRead)
async def get_(facility_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_facility(db, facility_id)
    if not obj: raise HTTPException(404, "Facility not found")
    return obj

@router.post("/", response_model=FacilityRead, status_code=201)
async def create_(payload: FacilityCreate, db: AsyncSession = Depends(get_db)):
    return await create_facility(db, payload.model_dump())

@router.patch("/{facility_id}", response_model=FacilityRead)
async def update_(facility_id: int, payload: FacilityUpdate, db: AsyncSession = Depends(get_db)):
    obj = await update_facility(db, facility_id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(404, "Facility not found")
    return obj

@router.delete("/{facility_id}", status_code=204)
async def delete_(facility_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_facility(db, facility_id)
    if not ok: raise HTTPException(404, "Facility not found")
