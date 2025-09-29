from fastapi import FastAPI
from .routes import health

app = FastAPI(title="Powerbase API")

app.include_router(health.router, prefix="/health")

@app.get("/")
def root():
    return {"service": "powerbase-api", "status": "up"}