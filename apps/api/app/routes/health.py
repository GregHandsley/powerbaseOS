from fastapi import APIRouter, Depends
from starlette import status
from ..core.db import db_ready

router = APIRouter(tags=["health"])

@router.get("/live", status_code=status.HTTP_200_OK)
async def live():
    # Process is up
    return {"status": "ok"}

@router.get("/ready", status_code=status.HTTP_200_OK)
async def ready():
    # Validate DB connectivity
    ok = await db_ready()
    return {"status": "ok" if ok else "fail", "dependencies": {"db": ok}}