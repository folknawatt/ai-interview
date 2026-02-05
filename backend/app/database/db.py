"""
SQLModel database configuration for AI Interview system.

This module provides database session management and engine configuration
for the database used to store interview data persistently.
"""
import os
import json
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.config.settings import settings
from app.config.logging_config import get_logger

logger = get_logger(__name__)


# Database connection URL
SQLALCHEMY_DATABASE_URL = settings.database_url


def json_serializer(obj):
    """JSON serializer for SQLAlchemy ensuring non-ASCII characters are preserved."""
    return json.dumps(obj, ensure_ascii=False)


# Create Async Engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    json_serializer=json_serializer,
    future=True
)


async def get_db():
    """
    Dependency function to get async database session.

    Yields:
        AsyncSession: SQLAlchemy async database session
    """
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def seed_db(session: AsyncSession):
    """Seed database with questions from JSON if tables are empty."""
    try:
        from app.database.models import (  # noqa: F401
            JobRole,
            Question,
        )

        # Check if we need to seed
        result = await session.exec(select(JobRole))
        if result.first():
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
            session.add(role)
            # await session.flush() # Not strictly needed if we manage dependencies correctly, but useful if IDs are auto-generated and needed immediately

            for idx, q_text in enumerate(role_data.get("questions", [])):
                question = Question(
                    role_id=role_id, content=q_text, order=idx)
                session.add(question)

        await session.commit()
        logger.info("Database seeding completed.")
    except (OSError, json.JSONDecodeError) as e:
        logger.error("Error reading seed file: %s", e)
        # No rollback needed on read error, nothing added
    except SQLAlchemyError as e:
        logger.error("Database error during seeding: %s", e)
        await session.rollback()


async def seed_users(session: AsyncSession):
    """Seed default admin user."""
    from app.services.auth.auth_service import AuthService

    try:
        # We need to refactor AuthService to be async first, or call the logic directly here
        # For now, let's assume AuthService will be refactored or we do a direct check
        # This part might need adjustment after AuthService refactor.
        # Temporarily commenting out auth seeding until AuthService is async ready.
        # user = await AuthService.create_default_admin(session)
        await AuthService.create_default_admin(session)
    except Exception as e:
        logger.error("Error seeding users: %s", e)


async def init_db():
    """
    Initialize database by creating all tables.
    This should be called on application startup.
    """
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all) # For dev reset
        await conn.run_sync(SQLModel.metadata.create_all)

    # Seed data
    async with AsyncSession(engine, expire_on_commit=False) as session:
        await seed_db(session)
        await seed_users(session)  # Enable after Auth service refactor
