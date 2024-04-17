from logging import Logger
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.database import check_database_health
from src.dependencies import get_database_session, get_logger
from src.security.schemas.response.health import HealthCheckResponse


router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=HealthCheckResponse, responses={503: {"model": HealthCheckResponse}})
def health_check(db_session: Session = Depends(get_database_session), logger: Logger = Depends(get_logger)):
    logger = logger.getChild("health_check")
    logger.info(f"Retrieving Health Check")
    is_database_up, err_message = check_database_health(db_session)
    status_code = status.HTTP_200_OK 
    if is_database_up == False:
        logger.error('Error on connecting to Database')
        logger.error(err_message)
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    health = is_database_up
    response  = { 'success': health, 'up': { 'database': is_database_up } } 
    return JSONResponse(content=response, status_code=status_code)
