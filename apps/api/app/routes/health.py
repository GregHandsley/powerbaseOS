from fastapi import APIRouter

router = APIRouter()

@router.get("/live")
async def live():
    return {"status": "ok"}