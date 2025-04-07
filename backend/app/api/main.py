from fastapi import APIRouter

from app.api.routes import password

api_router = APIRouter()

api_router.include_router(password.router, prefix="/password", tags=["password"])