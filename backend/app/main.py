from fastapi import FastAPI

from app.routers import upload
from app.routers import chat

app = FastAPI(title="DocPilot API")

app.include_router(upload.router)
app.include_router(chat.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to DocPilot!"
    }