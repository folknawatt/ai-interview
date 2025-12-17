"""
SQLModel database configuration for AI Interview system.

This module provides database session management and engine configuration
for the database used to store interview data persistently.
"""
import os
import json
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.exc import SQLAlchemyError

from app.config.settings import settings
from app.config.logging_config import get_logger

logger = get_logger(__name__)


# Database connection URL
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
    with Session(engine) as session:
        yield session


def seed_db():
    """Seed database with questions from JSON if tables are empty."""

    with Session(engine) as db:
        try:

            from app.database.models import (  # noqa: F401
                JobRole,
                Question,
            )

            # Check if we need to seed
            if db.exec(select(JobRole)).first():
                return

            json_path = settings.questions_file_path
            if not os.path.exists(json_path):
                logger.warning("Seed file not found: %s", json_path)
                return

            logger.info("Seeding database from %s", json_path)
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for role_id, role_data in data.items():
                role = JobRole(
                    id=role_id,
                    title=role_data.get("title", role_id)
                )
                db.add(role)
                db.flush()  # Ensure role exists for FK

                for idx, q_text in enumerate(role_data.get("questions", [])):
                    question = Question(
                        role_id=role_id, content=q_text, order=idx)
                    db.add(question)

            db.commit()
            logger.info("Database seeding completed.")
        except (OSError, json.JSONDecodeError) as e:
            logger.error("Error reading seed file: %s", e)
            db.rollback()
        except SQLAlchemyError as e:
            logger.error("Database error during seeding: %s", e)
            db.rollback()


def init_db():
    """
    Initialize database by creating all tables.

    This should be called on application startup.
    """
    # Models are now registered with SQLModel.metadata
    SQLModel.metadata.create_all(bind=engine)

    # Seed initial data
    seed_db()
