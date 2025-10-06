import asyncio
from sqlalchemy import select
from app.core.db import SessionLocal
from app.models.user import User, Role
from app.core.security import get_password_hash

DEFAULT_ROLES = ["ADMIN", "STAFF", "KIOSK", "PUBLIC"]

async def seed():
    async with SessionLocal() as db:
        # Roles
        res = await db.execute(select(Role))
        existing = {r.name for r in res.scalars().all()}
        for name in DEFAULT_ROLES:
            if name not in existing:
                db.add(Role(name=name))
        await db.flush()

        # Helper to get role objects
        res = await db.execute(select(Role))
        roles_by_name = {r.name: r for r in res.scalars().all()}

        # Users
        async def ensure_user(email: str, password: str, full_name: str, role_names: list[str]):
            res = await db.execute(select(User).where(User.email == email))
            user = res.scalar_one_or_none()
            if not user:
                user = User(
                    email=email,
                    full_name=full_name,
                    password_hash=get_password_hash(password),
                    is_active=True
                )
                user.roles = [roles_by_name[r] for r in role_names]
                db.add(user)

        await ensure_user("admin@example.com", "admin", "Administrator", ["ADMIN"])
        await ensure_user("kiosk@example.com", "kiosk", "Kiosk Device", ["KIOSK"])

        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed())