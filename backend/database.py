from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.config import get_settings

engine = create_engine(
    get_settings().db_url, connect_args={"check_same_thread":False}
)

LocalSession = sessionmaker(
    autoflush=False, bind=engine
)
Base = declarative_base()