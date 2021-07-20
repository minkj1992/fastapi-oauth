from fastapi import APIRouter

from src.apps.api.v1.auth import auth_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router, tags=["oauth"])
