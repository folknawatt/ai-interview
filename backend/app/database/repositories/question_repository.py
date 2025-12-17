"""
Question Repository for Question storage in Database.

This module provides a repository pattern for managing interview questions
stored in the relational database.
"""
from typing import Any, Dict, List, Optional
from sqlmodel import Session, select

from app.config.logging_config import get_logger

from app.database.db import engine
from app.database.models import JobRole, Question

logger = get_logger(__name__)


class QuestionRepository:
    """Repository for managing interview questions in the database."""

    def __init__(self):
        """Initialize question repository."""
        self.engine = engine

    def load_all(self) -> Dict[str, Any]:
        """
        Load all roles and questions from the database.

        Returns:
            Dict[str, Any]: A dictionary where keys are role IDs and values
                are dictionaries containing 'title' and a list of 'questions'.

                Example:
                {
                    "role_id": {
                        "title": "Role Title",
                        "questions": ["Question 1", "Question 2"]
                    }
                }
        """

        with Session(self.engine) as session:
            # SQLModel style: exec(select(...))
            roles = session.exec(select(JobRole)).all()
            result = {}
            for role in roles:
                # Relationship loading is standard SQLAlchemy/SQLModel behavior
                # lazy loading should work if session is open
                # Or explicit query:
                statement = (
                    select(Question)
                    .where(Question.role_id == role.id)
                    .order_by(Question.order)
                )
                questions = session.exec(statement).all()

                result[role.id] = {
                    "title": role.title,
                    "questions": [{"id": q.id, "content": q.content} for q in questions]
                }
            return result

    def save(self, role_id: str, title: str, questions: List[str]) -> None:
        """
        Save questions for a specific role (Create or Update).

        Args:
            role_id (str): Unique identifier for the job role.
            title (str): Display title for the role.
            questions (List[str]): List of question strings to associate
                with the role.

        Raises:
            RuntimeError: If the database operation fails.
        """
        with Session(self.engine) as session:
            try:
                role = session.exec(select(JobRole).where(
                    JobRole.id == role_id)).first()
                if not role:
                    role = JobRole(id=role_id, title=title)
                    session.add(role)
                else:
                    role.title = title

                # Flush to ensure role exists if created
                session.flush()

                # Clear existing questions to replace
                statement = select(Question).where(
                    Question.role_id == role_id
                )
                results = session.exec(statement).all()
                for q in results:
                    session.delete(q)

                for idx, q_text in enumerate(questions):
                    q = Question(role_id=role_id, content=q_text, order=idx)
                    session.add(q)

                session.commit()
                logger.info(
                    "Saved role %s with %s questions",
                    role_id,
                    len(questions)
                )
            except (ValueError, RuntimeError) as e:
                session.rollback()
                logger.error("Failed to save role %s: %s", role_id, e)
                raise RuntimeError(f"Database save failed: {e}") from e

    def get_by_id(self, role_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves role questions by role ID.

        Args:
            role_id (str): The role ID to search for.

        Returns:
            Optional[Dict[str, Any]]: A dictionary with 'title' and 'questions' keys,
                                      or None if the role is not found.
        """
        with Session(self.engine) as session:
            role = session.exec(select(JobRole).where(
                JobRole.id == role_id)).first()
            if not role:
                return None

            statement = (
                select(Question)
                .where(Question.role_id == role.id)
                .order_by(Question.order)
            )
            questions = session.exec(statement).all()

            return {
                "title": role.title,
                "questions": [{"id": q.id, "content": q.content} for q in questions]
            }

    def delete(self, role_id: str) -> bool:
        """
        Delete a role and its associated questions.

        Args:
            role_id (str): The ID of the role to delete.

        Returns:
            bool: True if the role was found and deleted, False otherwise.
        """
        with Session(self.engine) as session:
            role = session.exec(select(JobRole).where(
                JobRole.id == role_id)).first()
            if role:
                session.delete(role)  # Cascade should handle questions
                session.commit()
                return True
            return False

    def exists(self, role_id: str) -> bool:
        """
        Check if a role exists in the database.

        Args:
            role_id (str): The role ID to check.

        Returns:
            bool: True if the role exists, False otherwise.
        """
        with Session(self.engine) as session:
            role = session.exec(select(JobRole).where(
                JobRole.id == role_id)).first()
            return role is not None

    def update_questions(
        self, role_id: str, questions: List[str]
    ) -> None:
        """
        Update questions for an existing role.

        Args:
            role_id (str): The ID of the role to update.
            questions (List[str]): List of new question content strings.

        Raises:
            ValueError: If the role does not exist.
        """
        with Session(self.engine) as session:
            try:
                role = session.exec(select(JobRole).where(
                    JobRole.id == role_id)).first()
                if not role:
                    raise ValueError(f"Role '{role_id}' not found")

                # Simplistic approach: delete all and recreate
                existing_questions = session.exec(
                    select(Question).where(Question.role_id == role_id)
                ).all()
                for q in existing_questions:
                    session.delete(q)

                for idx, q_text in enumerate(questions):
                    q = Question(role_id=role_id, content=q_text, order=idx)
                    session.add(q)

                session.commit()
            except ValueError:
                session.rollback()
                raise
            except Exception as e:
                session.rollback()
                logger.error(
                    "Failed to update questions for role %s: %s",
                    role_id,
                    e
                )
                raise RuntimeError(
                    f"Database update failed: {e}"
                ) from e


# Singleton instance
_QUESTION_REPOSITORY = QuestionRepository()


def get_question_repository() -> QuestionRepository:
    """Get singleton instance of QuestionRepository."""
    return _QUESTION_REPOSITORY
