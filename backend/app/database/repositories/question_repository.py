"""
Question Repository for Question storage in Database.

This module provides a repository pattern for managing interview questions
stored in the relational database.
"""
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.config.logging_config import get_logger
from app.database.db import SessionLocal
from app.database.models import JobRole, Question

logger = get_logger(__name__)


class QuestionRepository:
    """Repository for managing interview questions in the database."""

    def __init__(self):
        """Initialize question repository."""
        self.db_factory = SessionLocal

    def _get_session(self) -> Session:
        """Get a new database session."""
        return self.db_factory()

    def load_all(self) -> Dict[str, Any]:
        """
        Load all roles and questions from the database.

        Returns:
            Dict[str, Any]: A dictionary where keys are role IDs and values are dictionaries
                            containing 'title' and a list of 'questions'.
                            Example:
                            {
                                "role_id": {
                                    "title": "Role Title",
                                    "questions": ["Question 1", "Question 2"]
                                }
                            }
        """
        session = self._get_session()
        try:
            roles = session.query(JobRole).all()
            result = {}
            for role in roles:
                questions = session.query(Question)\
                    .filter(Question.role_id == role.id)\
                    .order_by(Question.order)\
                    .all()

                result[role.id] = {
                    "title": role.title,
                    "questions": [q.content for q in questions]
                }
            return result
        finally:
            session.close()

    def save(self, role_id: str, title: str, questions: List[str]) -> None:
        """
        Save questions for a specific role (Create or Update).

        Args:
            role_id (str): Unique identifier for the job role.
            title (str): Display title for the role.
            questions (List[str]): List of question strings to associate with the role.

        Raises:
            RuntimeError: If the database operation fails.
        """
        session = self._get_session()
        try:
            role = session.query(JobRole).filter(JobRole.id == role_id).first()
            if not role:
                role = JobRole(id=role_id, title=title)
                session.add(role)
            else:
                role.title = title

            # Clear existing questions to replace (brute force update)
            session.query(Question).filter(
                Question.role_id == role_id).delete()

            for idx, q_text in enumerate(questions):
                q = Question(role_id=role_id, content=q_text, order=idx)
                session.add(q)

            session.commit()
            logger.info(
                f"Saved role {role_id} with {len(questions)} questions")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save role {role_id}: {e}")
            raise RuntimeError(f"Database save failed: {e}")
        finally:
            session.close()

    def get_by_id(self, role_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves role questions by role ID.

        Args:
            role_id (str): The role ID to search for.

        Returns:
            Optional[Dict[str, Any]]: A dictionary with 'title' and 'questions' keys,
                                      or None if the role is not found.
        """
        session = self._get_session()
        try:
            role = session.query(JobRole).filter(JobRole.id == role_id).first()
            if not role:
                return None

            questions = session.query(Question)\
                .filter(Question.role_id == role.id)\
                .order_by(Question.order)\
                .all()

            return {
                "title": role.title,
                "questions": [q.content for q in questions]
            }
        finally:
            session.close()

    def delete(self, role_id: str) -> bool:
        """
        Delete a role and its associated questions.

        Args:
            role_id (str): The ID of the role to delete.

        Returns:
            bool: True if the role was found and deleted, False otherwise.
        """
        session = self._get_session()
        try:
            role = session.query(JobRole).filter(JobRole.id == role_id).first()
            if role:
                session.delete(role)  # Cascade should handle questions
                session.commit()
                return True
            return False
        finally:
            session.close()

    def exists(self, role_id: str) -> bool:
        """
        Check if a role exists in the database.

        Args:
            role_id (str): The role ID to check.

        Returns:
            bool: True if the role exists, False otherwise.
        """
        session = self._get_session()
        try:
            return session.query(JobRole).filter(JobRole.id == role_id).count() > 0
        finally:
            session.close()

    def update_questions(self, role_id: str, questions: List[str]) -> None:
        """
        Update questions for an existing role.

        Args:
            role_id (str): The ID of the role to update.
            questions (List[str]): Loop of new question content strings.

        Raises:
            ValueError: If the role does not exist.
        """
        session = self._get_session()
        try:
            role = session.query(JobRole).filter(JobRole.id == role_id).first()
            if not role:
                raise ValueError(f"Role '{role_id}' not found")

            # Simplistic approach: delete all and recreate
            session.query(Question).filter(
                Question.role_id == role_id).delete()

            for idx, q_text in enumerate(questions):
                q = Question(role_id=role_id, content=q_text, order=idx)
                session.add(q)

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


# Singleton instance
_QUESTION_REPOSITORY = QuestionRepository()


def get_question_repository() -> QuestionRepository:
    """Get singleton instance of QuestionRepository."""
    return _QUESTION_REPOSITORY
