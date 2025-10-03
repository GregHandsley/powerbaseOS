from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import get_db
from app.models.side import Side
from app.schemas.side import SideCreate, SideUpdate, SideRead

router = APIRouter(prefix="/sides", tags=["sides"])

@router.get("/", response_model=list[SideRead])
async def list_(facility_id: int | None = Query(None), db: AsyncSession = Depends(get_db)):
    stmt = select(Side)
    if facility_id is not None:
        stmt = stmt.where(Side.facility_id == facility_id)
    res = await db.execute(stmt.order_by(Side.name))
    return res.scalars().all()

@router.get("/{side_id}", response_model=SideRead)
async def get_(side_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Side, side_id)
    if not obj: raise HTTPException(404, "Side not found")
    return obj

@router.post("/", response_model=SideRead, status_code=201)
async def create_(payload: SideCreate, db: AsyncSession = Depends(get_db)):
    obj = Side(**payload.model_dump())
    db.add(obj)
    await db.commit(); await db.refresh(obj)
    return obj

@router.patch("/{side_id}", response_model=SideRead)
async def update_(side_id: int, payload: SideUpdate, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Side, side_id)
    if not obj: raise HTTPException(404, "Side not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        if v is not None: setattr(obj, k, v)
    await db.commit(); await db.refresh(obj)
    return obj

@router.delete("/{side_id}", status_code=204)
async def delete_(side_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Side, side_id)
    if not obj: raise HTTPException(404, "Side not found")
    await db.delete(obj); await db.commit()
