from fastapi import FastAPI
from app.api import api_router

app = FastAPI(title="Organization Management API")

# Include routes
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Organization Management API"}
