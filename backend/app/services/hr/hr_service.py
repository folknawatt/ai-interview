"""
HR Service.

Encapsulates business logic for HR management, including:
- Question generation via AI
- Role and question management
- CRUD operations for roles
"""
from typing import Dict, Any, List

from app.database.repositories import get_question_repository
from app.services.interview.question_manager import gen_questions
from app.services.core.role_service import RoleService
from app.exceptions import NotFoundError


class HRService:
    """Service class for handling HR management business logic."""

    @staticmethod
    def generate_questions(
        api_key: str,
        role_title: str,
        job_description: str
    ) -> List[str]:
        """
        Generate interview questions from job description using AI.

        Args:
            api_key: API key for AI service
            role_title: Job role title
            job_description: Job description text

        Returns:
            List of generated questions
        """
        questions = gen_questions(api_key, role_title, job_description)
        return questions

    @staticmethod
    def save_role_questions(
        role_id: str,
        role_title: str,
        questions: List[str]
    ) -> Dict[str, str]:
        """
        Save approved interview questions to database.

        Args:
            role_id: Unique role identifier
            role_title: Job role title
            questions: List of questions

        Returns:
            Success status and message
        """
        repo = get_question_repository()
        repo.save(role_id, role_title, questions)
        return {
            "status": "success",
            "message": f"Saved questions for {role_title}"
        }

    @staticmethod
    def get_all_roles() -> List[Dict[str, str]]:
        """
        Get all job roles.

        Returns:
            List of roles with id and name
        """
        repo = get_question_repository()
        questions_db = repo.load_all()
        return [
            {"id": k, "title": v["title"]}
            for k, v in questions_db.items()
        ]

    @staticmethod
    def update_role_questions(
        role_id: str,
        questions: List[str]
    ) -> Dict[str, str]:
        """
        Update questions for an existing role.

        Args:
            role_id: Unique role identifier
            questions: New list of questions

        Returns:
            Success status and message

        Raises:
            NotFoundError: If role not found
        """
        repo = get_question_repository()

        # Check existence via RoleService
        if not RoleService.exists(role_id):
            raise NotFoundError(f"Role '{role_id}' not found")

        repo.update_questions(role_id, questions)
        role_data = RoleService.get_role_by_id(role_id)

        return {
            "status": "success",
            "message": f"Updated questions for {role_data['title']}"
        }

    @staticmethod
    def append_role_questions(
        role_id: str,
        questions: List[str]
    ) -> Dict[str, str]:
        """
        Append new questions to an existing role (keeps existing questions).

        Args:
            role_id: Unique role identifier
            questions: List of questions to append

        Returns:
            Success status and message

        Raises:
            NotFoundError: If role not found
        """
        repo = get_question_repository()

        if not RoleService.exists(role_id):
            raise NotFoundError(f"Role '{role_id}' not found")

        repo.append_questions(role_id, questions)
        role_data = RoleService.get_role_by_id(role_id)

        return {
            "status": "success",
            "message": f"Appended {len(questions)} questions to {role_data['title']}"
        }

    @staticmethod
    def delete_role(role_id: str) -> Dict[str, str]:
        """
        Delete a role completely.

        Args:
            role_id: Unique role identifier

        Returns:
            Success status and message

        Raises:
            NotFoundError: If role not found
        """
        repo = get_question_repository()

        # Check existence first
        if not repo.exists(role_id):
            raise NotFoundError(f"Role '{role_id}' not found")

        # Get title for success message (fallback to role_id if not found)
        role_title = RoleService.get_role_title(role_id)

        repo.delete(role_id)

        return {
            "status": "success",
            "message": f"Deleted role: {role_title}"
        }

    @staticmethod
    def create_candidate_role(base_role_id: str, unique_suffix: str) -> str:
        """
        Create a candidate-specific role by cloning a base role.

        DEPRECATED: This method implements the "Duplicate Role" anti-pattern.
        Use InterviewService.init_session_with_questions() (Snapshot Pattern) instead.
        """
        # Deprecated logic removed to prevent accidental use
        raise NotImplementedError(
            "create_candidate_role is deprecated. Use InterviewService.init_session_with_questions() instead."
        )
