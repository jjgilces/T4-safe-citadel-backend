"""
Database Configuration
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
DATABASE_URL = os.environ.get("DATABASE_URL")
#DATABASE_URL = "postgresql://sfe:sfe@localhost/backend"
DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL)

Base = declarative_base()


def get_session() -> sessionmaker:
    """
    Get a new database session.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
