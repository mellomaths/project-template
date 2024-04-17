from functools import lru_cache
from pydantic import BaseSettings
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel


load_dotenv(find_dotenv())


class Environment(BaseSettings):
    py_env: str = "local" # "dev" | "prod"
    service_name: str = "fastapi"
    api_version: str = "v1"
    port: int = 4000
    api_host: str = "http://localhost:4000"
    database_url: str = "sqlite:///./app.db"
    token_crypt_private_key: str

    @property
    def is_production(self) -> bool:
        return self.py_env.lower() == 'prod'
    
    @staticmethod
    @lru_cache()
    def load():
        return Environment()
