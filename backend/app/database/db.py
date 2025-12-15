"""
SQLAlchemy database configuration for AI Interview system.

This module provides database session management and engine configuration
for the database used to store interview results and scores persistently.
"""
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.config.settings import settings
# Import all models to register them with SQLAlchemy Base.metadata
# These imports are necessary for table creation and ORM functionality
from app.database.models import (  # noqa: F401
    JobRole,
    Question,
)

SQLALCHEMY_DATABASE_URL = settings.database_url


def json_serializer(obj):
    """JSON serializer for SQLAlchemy ensuring non-ASCII characters are preserved."""
    return json.dumps(obj, ensure_ascii=False)


# Create engine with PostgreSQL configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,  # Set to True for SQL query logging during development
    json_serializer=json_serializer
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


def seed_db():
    """Seed database with questions from JSON if tables are empty."""
    db = SessionLocal()
    try:
        # Check if we need to seed
        if db.query(JobRole).first():
            return

        json_path = settings.questions_file_path
        if not os.path.exists(json_path):
            print(f"Seed file not found: {json_path}")
            return

        print(f"Seeding database from {json_path}")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for role_id, role_data in data.items():
            role = JobRole(id=role_id, title=role_data.get("title", role_id))
            db.add(role)
            db.flush()  # Ensure role exists for FK

            for idx, q_text in enumerate(role_data.get("questions", [])):
                question = Question(role_id=role_id, content=q_text, order=idx)
                db.add(question)

        db.commit()
        print("Database seeding completed.")
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading seed file: {e}")
        db.rollback()
    except SQLAlchemyError as e:
        print(f"Database error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.

    This should be called on application startup.
    """
    # Models are now registered with Base.metadata
    Base.metadata.create_all(bind=engine)

    # Seed initial data
    seed_db()
