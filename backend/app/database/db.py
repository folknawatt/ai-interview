"""SQLModel database configuration for AI Interview system.

This module provides database session management and engine configuration
for the database used to store interview data persistently.
"""

import json
import os

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config.logging_config import get_logger
from app.config.settings import settings

logger = get_logger(__name__)


# Database connection URL from settings (postgresql+asyncpg for async support)
SQLALCHEMY_DATABASE_URL = settings.database_url


def json_serializer(obj):
    """Custom JSON serializer for SQLAlchemy.

    Ensures non-ASCII characters (e.g., Thai, Chinese) are preserved correctly
    in JSON columns instead of being escaped as Unicode sequences.
    """
    return json.dumps(obj, ensure_ascii=False)


# ============================================================================
# Async Database Engine
# ============================================================================
# Create async engine for PostgreSQL using asyncpg driver
# - echo=False: Disable SQL query logging (set True for debugging)
# - json_serializer: Custom serializer to properly handle non-ASCII text
# - future=True: Use SQLAlchemy 2.0 style (required for async)
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=False, json_serializer=json_serializer, future=True
)


async def get_db():
    """FastAPI dependency to provide async database sessions.

    This is a generator function that yields a session and automatically handles:
    - Session creation from the async engine
    - Session cleanup after request completes (via finally block implicit in async context)

    expire_on_commit=False: Prevents SQLModel objects from being expired after commit,
    allowing us to access them outside the session/request context if needed.

    Yields:
        AsyncSession: SQLAlchemy async database session for the request lifecycle
    """
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def seed_db(session: AsyncSession):
    """Seed database with initial roles and questions from JSON file.

    This runs on application startup to populate the database if it's empty.
    Questions are loaded from a JSON file (questions_db.json) which defines
    base questions for each job role (e.g., marketing, engineering).

    The seeding is idempotent - it only runs if the JobRole table is empty.
    """
    try:
        from app.database.models import (  # noqa: F401
            JobRole,
            Question,
        )

        # Check if database is already seeded (avoid duplicate data)
        result = await session.exec(select(JobRole))
        if result.first():
            # Database already has roles, skip seeding
            return

        # Load seed data from JSON file
        json_path = settings.questions_file_path
        if not os.path.exists(json_path):
            logger.warning("Seed file not found: %s", json_path)
            return

        logger.info("Seeding database from %s", json_path)
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        # Iterate through roles and their questions
        for role_id, role_data in data.items():
            # Create job role (e.g., "marketing", "engineer")
            role = JobRole(id=role_id, title=role_data.get("title", role_id))
            session.add(role)

            # Create questions for this role in order
            for idx, q_text in enumerate(role_data.get("questions", [])):
                question = Question(role_id=role_id, content=q_text, order=idx)
                session.add(question)

        # Persist all roles and questions to database
        await session.commit()
        logger.info("Database seeding completed.")

    except (OSError, json.JSONDecodeError) as e:
        # File I/O or JSON parsing errors - no database rollback needed
        logger.error("Error reading seed file: %s", e)

    except SQLAlchemyError as e:
        # Database errors - rollback to prevent partial data
        logger.error("Database error during seeding: %s", e)
        await session.rollback()


async def seed_users(session: AsyncSession):
    """Seed default admin user for initial system access.

    Creates or updates the admin user with credentials from environment variables.
    This ensures there's always an admin account available for system setup.
    """
    from app.services.auth.auth_service import AuthService

    try:
        # Create/update default admin user from settings
        await AuthService.create_default_admin(session)
    except Exception as e:
        # Log error but don't crash startup - user can manually create admin later
        logger.error("Error seeding users: %s", e)


async def init_db():
    """Initialize database schema on application startup.

    This function:
    1. Creates all tables defined in SQLModel models
    2. Seeds initial data (roles, questions, admin user)

    Called during application lifespan startup in main.py.
    """
    # Create all tables from SQLModel.metadata
    async with engine.begin() as conn:
        # Uncomment for development to reset database on each startup:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    # Seed initial data using a new session
    async with AsyncSession(engine, expire_on_commit=False) as session:
        await seed_db(session)  # Seed roles and questions
        await seed_users(session)  # Seed default admin user
