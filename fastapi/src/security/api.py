from fastapi import APIRouter, Depends

from src.security.routers import health

from src.auth import grant_access_to_api_user


PROTECTED = [Depends(grant_access_to_api_user)]


router = APIRouter()

router.include_router(health.router)
