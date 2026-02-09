"""
Role Service.

Centralizes business logic for Role retrieval and validation to avoid redundancy
between HRService and QuestionService.
"""
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.question_repository import get_question_repository
from app.exceptions import NotFoundError


class RoleService:
    """Service class for handling clean Role operations."""

    @staticmethod
    async def get_role_by_id(session: AsyncSession, role_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific role.

        Args:
            session: Database session
            role_id: Unique role identifier

        Returns:
            Role details including questions

        Raises:
            NotFoundError: If role not found
        """
        repo = get_question_repository()
        role_data = await repo.get_by_id(session, role_id)

        if not role_data:
            raise NotFoundError(f"Role '{role_id}' not found")

        return {
            "id": role_id,
            "title": role_data["title"],
            "questions": role_data["questions"]
        }

    @staticmethod
    async def exists(session: AsyncSession, role_id: str) -> bool:
        """
        Check if a role exists.
        """
        repo = get_question_repository()
        return await repo.exists(session, role_id)

    @staticmethod
    async def get_role_title(session: AsyncSession, role_id: str) -> str:
        """
        Get the human-readable title for a role.
        """
        repo = get_question_repository()
        role_data = await repo.get_by_id(session, role_id)

        if role_data and "title" in role_data:
            return role_data["title"]
        return role_id
