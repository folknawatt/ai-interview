"""
HR Service.

Encapsulates business logic for HR management, including:
- Question generation via AI
- Role and question management
- CRUD operations for roles
"""
from typing import Dict, Any, List

from app.database.repositories import get_question_repository
from app.domain.interview.question_manager import gen_questions
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
            {"id": k, "name": v["title"]}
            for k, v in questions_db.items()
        ]

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

        if not repo.exists(role_id):
            raise NotFoundError(f"Role '{role_id}' not found")

        repo.update_questions(role_id, questions)
        role_data = repo.get_by_id(role_id)

        return {
            "status": "success",
            "message": f"Updated questions for {role_data['title']}"
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
        role_data = repo.get_by_id(role_id)

        if not role_data:
            raise NotFoundError(f"Role '{role_id}' not found")

        role_title = role_data["title"]
        repo.delete(role_id)

        return {
            "status": "success",
            "message": f"Deleted role: {role_title}"
        }
