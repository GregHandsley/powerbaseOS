from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes import health
from .core.logging import setup_logging
from .core.db import lifespan_db_check

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Configure logging once (on reload, uvicorn may call this again)
    setup_logging()
    # Ensure DB connectivity at boot
    async with lifespan_db_check():
        yield

app = FastAPI(title="Powerbase API", lifespan=lifespan)

# routes
app.include_router(health.router, prefix="/health")

@app.get("/")
def root():
    return {"service": "powerbase-api", "status": "up"}