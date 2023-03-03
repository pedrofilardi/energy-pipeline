from fastapi import FastAPI
from app.routers.generation import router as generation_router


app = FastAPI()


app.include_router(generation_router, prefix="/generation",
tags=["generation"])

