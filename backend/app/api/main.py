from fastapi import APIRouter

from app.api.routes import password, utils

api_router = APIRouter()

api_router.include_router(
    password.router, prefix="/password", tags=["password"]
)
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
