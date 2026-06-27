from fastapi import FastAPI

app = FastAPI(title="DocPilot API")


@app.get("/")
def home():
    return {
        "message": "Welcome to DocPilot!"
    }