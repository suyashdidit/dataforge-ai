from fastapi import FastAPI

from app.api.routes import router as routes_router
from app.api.scan import router as scan_router
from app.api.sql import router as sql_router

app = FastAPI(title="DataForge AI Backend")
app.include_router(routes_router)
app.include_router(sql_router)
app.include_router(scan_router)


@app.get("/")
def root() -> dict:
    return {"status": "ok"}
