"""
Question Service.

Encapsulates business logic for question management, including:
- Question retrieval for roles
- Next question sequencing
- Role validation
"""
from typing import Dict, Any, List, Optional

from app.database.repositories import get_question_repository
from app.exceptions import NotFoundError


class QuestionService:
    """Service class for handling question management business logic."""

    @staticmethod
    def get_questions_for_role(role_id: str) -> List[str]:
        """
        Get all questions for a specific role.

        Args:
            role_id: Unique role identifier

        Returns:
            List of questions

        Raises:
            NotFoundError: If role not found
        """
        repo = get_question_repository()
        role_data = repo.get_by_id(role_id)

        if not role_data:
            raise NotFoundError(f"Role '{role_id}' not found")

        return role_data.get("questions", [])

    @staticmethod
    def get_next_question(
        role_id: str,
        index: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get the next interview question or finish status.

        Args:
            role_id: Unique role identifier
            index: Question index (0-based)

        Returns:
            Dictionary with status and question info, or None if role not found
        """
        repo = get_question_repository()
        role_data = repo.get_by_id(role_id)

        if not role_data:
            return None

        questions = role_data["questions"]
        if index < len(questions):
            return {
                "status": "continue",
                "question": questions[index],
                "total": len(questions)
            }
        return {"status": "finished"}

    @staticmethod
    def validate_role_exists(role_id: str) -> bool:
        """
        Validate that a role exists.

        Args:
            role_id: Unique role identifier

        Returns:
            True if role exists, False otherwise
        """
        repo = get_question_repository()
        return repo.exists(role_id)

    @staticmethod
    def get_total_questions(role_id: str) -> int:
        """
        Get total number of questions for a role.

        Args:
            role_id: Unique role identifier

        Returns:
            Number of questions

        Raises:
            NotFoundError: If role not found
        """
        repo = get_question_repository()
        role_data = repo.get_by_id(role_id)

        if not role_data:
            raise NotFoundError(f"Role '{role_id}' not found")

        return len(role_data.get("questions", []))
