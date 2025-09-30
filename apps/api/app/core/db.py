from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from .settings import get_settings

_settings = get_settings()

engine = create_async_engine(
    _settings.database_url_async,
    echo=False,              # set True for SQL echo during development
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

@asynccontextmanager
async def lifespan_db_check() -> AsyncIterator[None]:
    # Optional: ensure we can talk to the DB at startup
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    yield
    # Optional: graceful engine dispose at shutdown
    await engine.dispose()

# Dependency for request-scoped DB sessions
async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session

# Helper for readiness endpoint
async def db_ready() -> bool:
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False