"""
HR Service.

Encapsulates business logic for HR management, including:
- Question generation via AI
- Role and question management
- CRUD operations for roles
"""
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession

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
        (Remains sync or can be async enabled if gen_questions supports it.
         For now, the AI call is likely blocking, so running in threadpool is option,
         but let's keep it simple if it's external API call. 
         Wait, gen_questions uses google.generativeai which might be sync. 
         Ideally this should be wrapped in asyncio.to_thread, but user asked for DB fix principally.
         However, let's keep it sync for now as it doesn't touch DB, or make it async if we want consistency).

         Actually, let's keep it sync for now as it doesn't touch the DB and user didn't request AI refactor.
        """
        response = gen_questions(api_key, role_title, job_description)
        return response.questions

    @staticmethod
    async def save_role_questions(
        session: AsyncSession,
        role_id: str,
        role_title: str,
        questions: List[str]
    ) -> Dict[str, str]:
        """
        Save approved interview questions to database.
        """
        repo = get_question_repository()
        await repo.save(session, role_id, role_title, questions)
        return {
            "status": "success",
            "message": f"Saved questions for {role_title}"
        }

    @staticmethod
    async def get_all_roles(session: AsyncSession) -> List[Dict[str, Any]]:
        """
        Get all job roles with details.
        """
        repo = get_question_repository()
        questions_db = await repo.load_all(session)
        return [
            {
                "id": k,
                "title": v.get("title", "Unknown Role"),
                "question_count": len(v.get("questions", [])),
                "questions": v.get("questions", [])
            }
            for k, v in questions_db.items()
        ]

    @staticmethod
    async def update_role_questions(
        session: AsyncSession,
        role_id: str,
        questions: List[str] | None = None,
        title: str | None = None
    ) -> Dict[str, str]:
        """
        Update details for an existing role.
        """
        repo = get_question_repository()

        # Check existence via Repo directly
        exists = await repo.exists(session, role_id)
        if not exists:
            raise NotFoundError(f"Role '{role_id}' not found")

        await repo.update_role(session, role_id, questions=questions, title=title)

        # RoleService is strictly file based? No. RoleService logic is weirdly circular.
        # "RoleService.get_role_by_id(role_id)" was used in sync code.
        # Let's see what RoleService does. If it just reads JSON, it's fine.
        # But if we are moving to DB, we should read from DB.
        # In this refactor, we should rely on what we just updated or fetch from repo.

        # Fetched updated role data from Repo strictly to avoid confusion
        updated_role_data = await repo.get_by_id(session, role_id)
        current_title = updated_role_data['title'] if updated_role_data else title

        return {
            "status": "success",
            "message": f"Updated details for {current_title}"
        }

    @staticmethod
    async def append_role_questions(
        session: AsyncSession,
        role_id: str,
        questions: List[str]
    ) -> Dict[str, str]:
        """
        Append new questions to an existing role (keeps existing questions).
        """
        repo = get_question_repository()

        exists = await repo.exists(session, role_id)
        if not exists:
            raise NotFoundError(f"Role '{role_id}' not found")

        await repo.append_questions(session, role_id, questions)

        updated_role_data = await repo.get_by_id(session, role_id)
        current_title = updated_role_data['title'] if updated_role_data else role_id

        return {
            "status": "success",
            "message": f"Appended {len(questions)} questions to {current_title}"
        }

    @staticmethod
    async def delete_role(session: AsyncSession, role_id: str) -> Dict[str, str]:
        """
        Delete a role completely.
        """
        repo = get_question_repository()

        # Check existence first, get title for message
        role_data = await repo.get_by_id(session, role_id)
        if not role_data:
            raise NotFoundError(f"Role '{role_id}' not found")

        role_title = role_data.get('title', role_id)

        await repo.delete(session, role_id)

        return {
            "status": "success",
            "message": f"Deleted role: {role_title}"
        }
