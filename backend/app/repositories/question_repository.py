"""
Question Repository for Question storage in Database.

This module provides a repository pattern for managing interview questions
stored in the relational database.
"""
from typing import Any, Dict, List, Optional
from sqlmodel import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlmodel.ext.asyncio.session import AsyncSession # We use the one that supports exec if using SQLModel

from app.config.logging_config import get_logger
from app.database.models import JobRole, Question

logger = get_logger(__name__)


class QuestionRepository:
    """Repository for managing interview questions in the database."""

    def __init__(self):
        """Initialize question repository."""
        # Session is now injected per method call
        pass

    async def load_all(self, session: AsyncSession) -> Dict[str, Any]:
        """
        Load all roles and questions from the database.
        """
        # SQLModel style: exec(select(...))
        result = await session.exec(select(JobRole))
        roles = result.all()

        output = {}
        for role in roles:
            # Relationship loading
            statement = (
                select(Question)
                .where(Question.role_id == role.id)
                .order_by(Question.order)
            )
            q_result = await session.exec(statement)
            questions = q_result.all()

            output[role.id] = {
                "title": role.title,
                "questions": [{"id": q.id, "content": q.content} for q in questions]
            }
        return output

    async def save(self, session: AsyncSession, role_id: str, title: str, questions: List[str]) -> None:
        """
        Save questions for a specific role (Create or Update).
        """
        try:
            r_result = await session.exec(select(JobRole).where(JobRole.id == role_id))
            role = r_result.first()

            if not role:
                role = JobRole(id=role_id, title=title)
                session.add(role)
            else:
                role.title = title

            # Flush to ensure role exists if created (async flush not always strict requirement but good practice)
            await session.flush()

            # Clear existing questions to replace
            statement = select(Question).where(
                Question.role_id == role_id
            )
            q_result = await session.exec(statement)
            results = q_result.all()
            for q in results:
                await session.delete(q)

            for idx, q_text in enumerate(questions):
                q = Question(role_id=role_id, content=q_text, order=idx)
                session.add(q)

            await session.commit()
            logger.info(
                "Saved role %s with %s questions",
                role_id,
                len(questions)
            )
        except (ValueError, RuntimeError) as e:
            await session.rollback()
            logger.error("Failed to save role %s: %s", role_id, e)
            raise RuntimeError(f"Database save failed: {e}") from e

    async def get_by_id(self, session: AsyncSession, role_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves role questions by role ID.
        """
        r_result = await session.exec(select(JobRole).where(JobRole.id == role_id))
        role = r_result.first()

        if not role:
            return None

        statement = (
            select(Question)
            .where(Question.role_id == role.id)
            .order_by(Question.order)
        )
        q_result = await session.exec(statement)
        questions = q_result.all()

        return {
            "title": role.title,
            "questions": [{"id": q.id, "content": q.content} for q in questions]
        }

    async def delete(self, session: AsyncSession, role_id: str) -> bool:
        """
        Delete a role and its associated questions.
        """
        r_result = await session.exec(select(JobRole).where(JobRole.id == role_id))
        role = r_result.first()

        if role:
            await session.delete(role)  # Cascade should handle questions
            await session.commit()
            return True
        return False

    async def exists(self, session: AsyncSession, role_id: str) -> bool:
        """
        Check if a role exists in the database.
        """
        r_result = await session.exec(select(JobRole).where(JobRole.id == role_id))
        role = r_result.first()
        return role is not None

    async def update_role(
        self,
        session: AsyncSession,
        role_id: str,
        questions: Optional[List[str]] = None,
        title: Optional[str] = None
    ) -> None:
        """
        Update details (title, questions) for an existing role.
        """
        try:
            r_result = await session.exec(select(JobRole).where(JobRole.id == role_id))
            role = r_result.first()

            if not role:
                raise ValueError(f"Role '{role_id}' not found")

            if title is not None:
                role.title = title
                session.add(role)

            if questions is not None:
                # Simplistic approach: delete all and recreate
                q_result = await session.exec(
                    select(Question).where(Question.role_id == role_id)
                )
                existing_questions = q_result.all()

                for q in existing_questions:
                    await session.delete(q)

                for idx, q_text in enumerate(questions):
                    q = Question(role_id=role_id,
                                 content=q_text, order=idx)
                    session.add(q)

            await session.commit()
        except ValueError:
            await session.rollback()
            raise
        except Exception as e:
            await session.rollback()
            logger.error(
                "Failed to update role %s: %s",
                role_id,
                e
            )
            raise RuntimeError(
                f"Database update failed: {e}"
            ) from e

    async def append_questions(
        self,
        session: AsyncSession,
        role_id: str,
        questions: List[str]
    ) -> None:
        """
        Append new questions to an existing role (keeps existing questions).
        """
        try:
            r_result = await session.exec(select(JobRole).where(JobRole.id == role_id))
            role = r_result.first()

            if not role:
                raise ValueError(f"Role '{role_id}' not found")

            # Get the current max order to continue from
            q_result = await session.exec(
                select(Question)
                .where(Question.role_id == role_id)
                .order_by(desc(Question.order))
            )
            existing_question = q_result.first()

            start_order = 0
            if existing_question:
                start_order = existing_question.order + 1

            # Append new questions after existing ones
            for idx, q_text in enumerate(questions):
                q = Question(
                    role_id=role_id,
                    content=q_text,
                    order=start_order + idx
                )
                session.add(q)

            await session.commit()
            logger.info(
                "Appended %s questions to role %s",
                len(questions),
                role_id
            )
        except ValueError:
            await session.rollback()
            raise
        except Exception as e:
            await session.rollback()
            logger.error(
                "Failed to append questions for role %s: %s",
                role_id,
                e
            )
            raise RuntimeError(
                f"Database append failed: {e}"
            ) from e

    def duplicate_role(self, base_role_id: str, new_role_id: str, new_title: str) -> None:
        """
        Duplicate an existing role and all its questions.

        DEPRECATED: This method supports the "Duplicate Role" anti-pattern.
        Do not use this for candidate sessions.
        """
        # Deprecated logic removed
        raise NotImplementedError(
            "duplicate_role is deprecated. Use Snapshot Pattern via QuestionResult instead."
        )


# Singleton instance
_QUESTION_REPOSITORY = QuestionRepository()


def get_question_repository() -> QuestionRepository:
    """Get singleton instance of QuestionRepository."""
    return _QUESTION_REPOSITORY
