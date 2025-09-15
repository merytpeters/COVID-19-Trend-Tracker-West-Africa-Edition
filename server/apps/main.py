"""Main entry point for App"""

from fastapi import FastAPI
from mangum import Mangum
from apps.api.routes import router as trend_router


app = FastAPI(title="COVID-19 Trend Tracker (West Africa Edition)")


@app.get("/")
def home():
    """Return Hello"""
    return {"message": "Hello"}


@app.get("/health")
def health():
    """Return Status Ok"""
    return {"status": "ok"}


app.include_router(trend_router, prefix="/api")

# Lambda handler
handler = Mangum(app)
