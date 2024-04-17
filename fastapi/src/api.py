from fastapi import APIRouter, Depends

from src.security.api import router as security_router
from src.auth import grant_access_to_api_user

router = APIRouter(redirect_slashes=False)

PROTECTED = [Depends(grant_access_to_api_user)]

router.include_router(security_router.router, prefix='/security', tags=['security'])

