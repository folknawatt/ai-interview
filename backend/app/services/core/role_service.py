"""
Role Service.

Centralizes business logic for Role retrieval and validation to avoid redundancy
between HRService and QuestionService.
"""
from typing import Dict, Any, List

from app.database.repositories import get_question_repository
from app.exceptions import NotFoundError


class RoleService:
    """Service class for handling clean Role operations."""

    @staticmethod
    def get_role_by_id(role_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific role.

        Args:
            role_id: Unique role identifier

        Returns:
            Role details including questions

        Raises:
            NotFoundError: If role not found
        """
        repo = get_question_repository()
        role_data = repo.get_by_id(role_id)

        if not role_data:
            raise NotFoundError(f"Role '{role_id}' not found")

        return {
            "id": role_id,
            "title": role_data["title"],
            "questions": role_data["questions"]
        }

    @staticmethod
    def exists(role_id: str) -> bool:
        """
        Check if a role exists.

        Args:
            role_id: Unique role identifier

        Returns:
            True if role exists, False otherwise
        """
        repo = get_question_repository()
        return repo.exists(role_id)

    @staticmethod
    def get_role_title(role_id: str) -> str:
        """
        Get the human-readable title for a role.

        Args:
            role_id: Unique role identifier

        Returns:
            Role title string, or role_id if not found
        """
        repo = get_question_repository()
        role_data = repo.get_by_id(role_id)

        if role_data and "title" in role_data:
            return role_data["title"]
        return role_id
