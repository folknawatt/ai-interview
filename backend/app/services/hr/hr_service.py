"""HR Service.

Encapsulates business logic for HR management, including:
- Question generation via AI
- Role and question management
- CRUD operations for roles
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundError
from app.repositories.question_repository import get_question_repository
from app.services.interview.question_manager import gen_questions


class HRService:
    """Service class for handling HR management business logic."""

    @staticmethod
    def generate_questions(api_key: str, role_title: str, job_description: str) -> list[str]:
        """Generate interview questions from job description using AI."""
        response = gen_questions(api_key, role_title, job_description)
        return response.questions

    @staticmethod
    async def save_role_questions(
        session: AsyncSession, role_id: str, role_title: str, questions: list[str]
    ) -> dict[str, str]:
        """Save approved interview questions to database."""
        repo = get_question_repository()
        await repo.save(session, role_id, role_title, questions)
        return {"status": "success", "message": f"Saved questions for {role_title}"}

    @staticmethod
    async def get_all_roles(session: AsyncSession) -> list[dict[str, Any]]:
        """Get all job roles with details."""
        repo = get_question_repository()
        questions_db = await repo.load_all(session)
        return [
            {
                "id": k,
                "title": v.get("title", "Unknown Role"),
                "question_count": len(v.get("questions", [])),
                "questions": v.get("questions", []),
            }
            for k, v in questions_db.items()
        ]

    @staticmethod
    async def update_role_questions(
        session: AsyncSession,
        role_id: str,
        questions: list[str] | None = None,
        title: str | None = None,
    ) -> dict[str, str]:
        """Update details for an existing role."""
        repo = get_question_repository()

        # Check existence via Repo directly
        exists = await repo.exists(session, role_id)
        if not exists:
            raise NotFoundError(f"Role '{role_id}' not found")

        await repo.update_role(session, role_id, questions=questions, title=title)

        # Fetched updated role data from Repo strictly to avoid confusion
        updated_role_data = await repo.get_by_id(session, role_id)
        current_title = updated_role_data["title"] if updated_role_data else title

        return {"status": "success", "message": f"Updated details for {current_title}"}

    @staticmethod
    async def append_role_questions(
        session: AsyncSession, role_id: str, questions: list[str]
    ) -> dict[str, str]:
        """Append new questions to an existing role (keeps existing questions)."""
        repo = get_question_repository()

        exists = await repo.exists(session, role_id)
        if not exists:
            raise NotFoundError(f"Role '{role_id}' not found")

        await repo.append_questions(session, role_id, questions)

        updated_role_data = await repo.get_by_id(session, role_id)
        current_title = updated_role_data["title"] if updated_role_data else role_id

        return {
            "status": "success",
            "message": f"Appended {len(questions)} questions to {current_title}",
        }

    @staticmethod
    async def delete_role(session: AsyncSession, role_id: str) -> dict[str, str]:
        """Delete a role completely."""
        repo = get_question_repository()

        # Check existence first, get title for message
        role_data = await repo.get_by_id(session, role_id)
        if not role_data:
            raise NotFoundError(f"Role '{role_id}' not found")

        role_title = role_data.get("title", role_id)

        await repo.delete(session, role_id)

        return {"status": "success", "message": f"Deleted role: {role_title}"}
