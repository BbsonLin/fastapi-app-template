from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

db_engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=db_engine)
