import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoint import router as api_router

app = FastAPI(title="Recipick AI Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("ALLOWED_ORIGINS", "http://localhost:8000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok"}