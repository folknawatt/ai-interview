
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.core.role_service import RoleService
from app.exceptions import NotFoundError


class QuestionService:
    """Service class for handling question management business logic."""

    @staticmethod
    async def get_questions_for_role(session: AsyncSession, role_id: str) -> List[str]:
        """
        Get all questions for a specific role.

        Args:
            session: Database session
            role_id: Unique role identifier

        Returns:
            List of questions
        """
        role_data = await RoleService.get_role_by_id(session, role_id)
        return role_data.get("questions", [])

    @staticmethod
    async def get_next_question(
        session: AsyncSession,
        role_id: str,
        index: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get the next interview question or finish status.

        Args:
            session: Database session
            role_id: Unique role identifier
            index: Question index (0-based)

        Returns:
            Dictionary with status and question info, or None if role not found
        """
        try:
            role_data = await RoleService.get_role_by_id(session, role_id)
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
    async def get_total_questions(session: AsyncSession, role_id: str) -> int:
        """
        Get total number of questions for a role.
        """
        role_data = await RoleService.get_role_by_id(session, role_id)
        return len(role_data.get("questions", []))

    @staticmethod
    async def get_session_question(
        session: AsyncSession,
        session_id: str,
        index: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get question from a specific interview session (Snapshot).

        Args:
            session: Async Database session
            session_id: Session ID
            index: Question index (0-based)
        """
        from app.repositories.interview_repository import InterviewRepository

        interview_repo = InterviewRepository(session)
        results = await interview_repo.get_session_questions_ordered(session_id)

        if not results:
            return None

        if index < len(results):
            qr = results[index]
            return {
                "status": "continue",
                "question": qr.question,
                "question_id": qr.id,
                "total": len(results),
                "session_id": session_id
            }

        return {"status": "finished"}
