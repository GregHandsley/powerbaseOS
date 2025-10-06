from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.security import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token,
    get_current_user, require_roles
)
from app.core.settings import get_settings
from app.models.user import User, Role
from app.schemas.user import LoginRequest, TokenPair, UserRead, RefreshRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(User).options(selectinload(User.roles)).where(User.email == payload.email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    roles = [r.name for r in user.roles]
    settings = get_settings()
    access = create_access_token(user.email, roles, settings.JWT_EXPIRES)
    refresh = create_refresh_token(user.email)
    return TokenPair(access_token=access, refresh_token=refresh, expires_in=settings.JWT_EXPIRES)

@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    from jose import jwt, JWTError
    settings = get_settings()
    try:
        payload_jwt = jwt.decode(payload.token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if payload_jwt.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    sub = payload_jwt.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    res = await db.execute(select(User).options(selectinload(User.roles)).where(User.email == sub))
    user = res.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User inactive or not found")

    roles = [r.name for r in user.roles]
    access = create_access_token(user.email, roles, get_settings().JWT_EXPIRES)
    new_refresh = create_refresh_token(user.email)
    return TokenPair(access_token=access, refresh_token=new_refresh, expires_in=get_settings().JWT_EXPIRES)

@router.get("/me", response_model=UserRead)
async def me(user: User = Depends(get_current_user)):
    return UserRead(
        id=user.id, email=user.email, full_name=user.full_name,
        is_active=user.is_active, roles=[r.name for r in user.roles]
    )

# Demo read-only endpoint for kiosks
@router.get("/kiosk-feed")
async def kiosk_feed(user: User = Depends(require_roles("KIOSK", "ADMIN", "STAFF"))):
    # minimal protected demo payload
    return {"ok": True, "who": user.email, "role_any_of": ["KIOSK", "ADMIN", "STAFF"]}