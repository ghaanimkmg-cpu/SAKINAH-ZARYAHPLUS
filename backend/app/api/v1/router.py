from fastapi import APIRouter
from app.api.v1 import health
from app.api.v1.nis import auth_test

api_router = APIRouter()
api_router.include_router(health.router, tags=['health'])
api_router.include_router(auth_test.router, prefix="/nis/auth", tags=['auth'])
