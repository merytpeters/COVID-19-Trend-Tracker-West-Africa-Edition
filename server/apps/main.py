"""Main entry point for App"""

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def home():
    """Return Hello"""
    return {"message": "Hello"}


@app.get("/health")
def health():
    """Return Status Ok"""
    return {"status": "ok"}
