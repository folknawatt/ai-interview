"""
SQLAlchemy database configuration for AI Interview system.

This module provides database session management and engine configuration
for SQLite database used to store interview results and scores persistently.
"""
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database file path in storage directory
DB_PATH = Path(__file__).parent.parent / "storage" / "ai_interview.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine with SQLite-specific configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False  # Set to True for SQL query logging during development
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.

    Yields:
        Session: SQLAlchemy database session

    Usage:
        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            # Use db here
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.

    This should be called on application startup.
    """
    # Import models to register them with SQLAlchemy Base
    from .models import Candidate, QuestionResult, AggregatedScore
    # Models are now registered with Base.metadata
    Base.metadata.create_all(bind=engine)
