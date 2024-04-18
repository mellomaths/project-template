from fastapi import APIRouter, Depends

from src.security import api as security_api
from src.auth import grant_access_to_api_user

router = APIRouter(redirect_slashes=False)

PROTECTED = [Depends(grant_access_to_api_user)]

router.include_router(security_api.router, prefix='/security', tags=['security'])

