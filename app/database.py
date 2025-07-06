"""
Database configuration and connection setup.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_USER, DB_HOST, DB_PORT, DB_NAME

# Database URL will be built with password parameter
def get_database_url(password: str) -> str:
    """Build database URL with password."""
    return f"postgresql://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def create_engine_with_password(password: str):
    """Create SQLAlchemy engine with password."""
    database_url = get_database_url(password)
    return create_engine(database_url)

# Create Base class
Base = declarative_base()

def get_db(password: str):
    """
    Dependency to get database session.
    """
    engine = create_engine_with_password(password)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db(password: str):
    """
    Initialize database tables.
    """
    engine = create_engine_with_password(password)
    Base.metadata.create_all(bind=engine) 