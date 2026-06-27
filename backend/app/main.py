from fastapi import FastAPI
from app.routers import upload

app = FastAPI(title="DocPilot API")

app.include_router(upload.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to DocPilot!"
    }