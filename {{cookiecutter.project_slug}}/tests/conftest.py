import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from app.database.base_class import Base
from app.config import settings


@pytest.fixture
def test_db():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(test_db):
    yield sessionmaker(bind=test_db)()
    clear_mappers()
