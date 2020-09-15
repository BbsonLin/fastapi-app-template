import os
import sys
import secrets
import logging

from typing import Optional
from loguru import logger
from pydantic import BaseSettings

from app.logger import InterceptHandler, format_record


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI: str = None
    SQLALCHEMY_DATABASE_URI_BASE: str = None

    POSTGRES_SERVER: Optional[str]
    POSTGRES_USER: Optional[str]
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_DB: Optional[str]

    LOG_LEVEL = logging.DEBUG


class Production(Settings):
    SQLALCHEMY_DATABASE_URI_BASE = 'postgres://postgres:dumppass@10.12.3.10:5433'
    LOG_LEVEL = logging.INFO

    def __init__(self):
        super(self.__class__, self).__init__()
        self.SQLALCHEMY_DATABASE_URI = f"{self.SQLALCHEMY_DATABASE_URI_BASE}/{self.POSTGRES_DB}"

    class Config:
        env_file = '.production.env'


class Development(Settings):
    SQLALCHEMY_DATABASE_URI_BASE = 'postgres://postgres:devpass@10.12.3.10:5433'

    def __init__(self):
        super(self.__class__, self).__init__()
        self.SQLALCHEMY_DATABASE_URI = f"{self.SQLALCHEMY_DATABASE_URI_BASE}/{self.POSTGRES_DB}"

    class Config:
        env_file = '.development.env'


class Testing(Settings):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./test.sqlite'


class LocalTesting(Settings):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./app.sqlite'

    class Config:
        env_file = '.local.env'


def get_settings():
    env = os.getenv('ENV', 'LOCAL')
    print('env:', env)
    if env == 'PRODUCTION':
        return Production()
    elif env == 'DEVELOPMENT':
        return Development()
    elif env == 'TESTING':
        return Testing()
    return LocalTesting()


settings = get_settings()

# Setup logging by loguru
# Ref: https://github.com/tiangolo/fastapi/issues/1276#issuecomment-615877177
logging.basicConfig(
    handlers=[InterceptHandler(level=settings.LOG_LEVEL)], level=settings.LOG_LEVEL
)
logger.configure(
    handlers=[
        {"sink": sys.stderr, "level": settings.LOG_LEVEL, "format": format_record},
        {"sink": "access.log", "level": settings.LOG_LEVEL, "format": format_record},
    ]
)
# set loguru handler for uvicorn logger.
logging.getLogger("uvicorn").handlers = [InterceptHandler()]
