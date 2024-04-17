import logging
from fastapi import Depends
from fastapi.security import HTTPBearer

from fastapi.src.environment import Environment
from src.database import SessionLocal


def get_database_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_environment():
    return Environment.load()


def get_logger(env: Environment = Depends(get_environment)):
    logging.basicConfig(level=logging.NOTSET)
    logger = logging.getLogger(env.service_name)
    return logger


def get_auth_scheme():
    token_auth_scheme = HTTPBearer()
    return token_auth_scheme
