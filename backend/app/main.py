from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncIterator
from .api.v1 import router as api_router
from .core.config import settings
from sqlmodel import SQLModel
from app.core.database import engine  

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan
)
app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:6626"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "running"}
