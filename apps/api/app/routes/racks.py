from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.rack import RackCreate, RackRead, RackUpdate
from app.services.racks import list_racks, get_rack, create_rack, update_rack, delete_rack

router = APIRouter(prefix="/racks", tags=["racks"])

@router.get("/", response_model=list[RackRead])
async def list_(side_id: int | None = Query(None), db: AsyncSession = Depends(get_db)):
    return await list_racks(db, side_id)

@router.get("/{rack_id}", response_model=RackRead)
async def get_(rack_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_rack(db, rack_id)
    if not obj: raise HTTPException(404, "Rack not found")
    return obj

@router.post("/", response_model=RackRead, status_code=201)
async def create_(payload: RackCreate, db: AsyncSession = Depends(get_db)):
    return await create_rack(db, payload.model_dump())

@router.patch("/{rack_id}", response_model=RackRead)
async def update_(rack_id: int, payload: RackUpdate, db: AsyncSession = Depends(get_db)):
    obj = await update_rack(db, rack_id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(404, "Rack not found")
    return obj

@router.delete("/{rack_id}", status_code=204)
async def delete_(rack_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_rack(db, rack_id)
    if not ok: raise HTTPException(404, "Rack not found")
