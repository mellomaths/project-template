from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from src.environment import Environment

SQLALCHEMY_DATABASE_URL = Environment.load().database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def check_database_health(session: Session):
    is_database_working = True
    output = 'OK'

    try:
        # to check database we will execute raw query
        session.execute('SELECT 1')
    except Exception as e:
        output = str(e)
        is_database_working = False

    return is_database_working, output
