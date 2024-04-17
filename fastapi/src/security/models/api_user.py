from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, JSON, Text, text, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

from src.database import Base

class ApiUser(Base):
    __tablename__ = 'api_user'

    id = Column(Integer, primary_key=True, server_default=text("nextval('api_user_id_seq'::regclass)"))
    created_at = Column(DateTime, server_default=text("now()"))
    name = Column(Text, unique=True)
    token = Column(Text)
    token_salt = Column(Text)
