
from typing import Dict, Any, List, Optional
from app.services.core.role_service import RoleService
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
        role_data = RoleService.get_role_by_id(role_id)
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
        try:
            role_data = RoleService.get_role_by_id(role_id)
        except NotFoundError:
            return None

        questions = role_data["questions"]
        if index < len(questions):
            q_data = questions[index]
            return {
                "status": "continue",
                "question": q_data["content"],
                "question_id": q_data["id"],
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
        return RoleService.exists(role_id)

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
        role_data = RoleService.get_role_by_id(role_id)
        return len(role_data.get("questions", []))

    @staticmethod
    def get_role_title(role_id: str) -> str:
        """
        Get the human-readable title for a role.

        Args:
            role_id: Unique role identifier

        Returns:
            Role title string, or role_id if not found
        """
        return RoleService.get_role_title(role_id)
