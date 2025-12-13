"""
Question Repository for JSON-based question storage.

This module provides a repository pattern for managing interview questions
stored in JSON files.
"""
import json
import os
from typing import Any, Dict, List

from app.config.logging_config import get_logger
from app.config.settings import settings

logger = get_logger(__name__)


class QuestionRepository:
    """Repository for managing interview questions in JSON storage."""

    def __init__(self):
        """Initialize question repository with database file path."""
        self.db_file = settings.database_file

    def load_all(self) -> Dict[str, Any]:
        """
        Load all roles and questions from JSON file.

        Returns:
            dict: Dictionary containing role questions, empty dict if file
                doesn't exist

        Example structure:
            {
                "role_id_1": {
                    "title": "Software Engineer",
                    "questions": ["Q1", "Q2", ...]
                }
            }
        """
        try:
            if not os.path.exists(self.db_file):
                logger.info(
                    "Database file not found, returning empty dict: %s",
                    self.db_file
                )
                return {}

            with open(self.db_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug("Loaded database with %d roles", len(data))
                return data
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON in %s: %s", self.db_file, e)
            return {}
        except (IOError, OSError) as e:
            logger.error("Failed to load database: %s", e)
            return {}

    def save(self, role_id: str, title: str, questions: List[str]) -> None:
        """
        Save questions for a specific role.

        Args:
            role_id: Unique role identifier
            title: Role title
            questions: List of interview questions

        Raises:
            RuntimeError: If file save operation fails
        """
        data = self.load_all()
        data[role_id] = {
            "title": title,
            "questions": questions
        }
        self._save_all(data)

    def get_by_id(self, role_id: str) -> Dict[str, Any] | None:
        """
        Get role questions by role ID.

        Args:
            role_id: Role identifier

        Returns:
            dict: Role data or None if not found
        """
        data = self.load_all()
        return data.get(role_id)

    def delete(self, role_id: str) -> bool:
        """
        Delete a role and its questions.

        Args:
            role_id: Role identifier

        Returns:
            bool: True if deleted, False if not found
        """
        data = self.load_all()
        if role_id in data:
            del data[role_id]
            self._save_all(data)
            return True
        return False

    def exists(self, role_id: str) -> bool:
        """
        Check if a role exists.

        Args:
            role_id: Role identifier

        Returns:
            bool: True if role exists
        """
        data = self.load_all()
        return role_id in data

    def update_questions(self, role_id: str, questions: List[str]) -> None:
        """
        Update questions for an existing role.

        Args:
            role_id: Role identifier
            questions: Updated list of questions

        Raises:
            ValueError: If role doesn't exist
        """
        data = self.load_all()
        if role_id not in data:
            raise ValueError(f"Role '{role_id}' not found")

        data[role_id]["questions"] = questions
        self._save_all(data)

    def _save_all(self, data: Dict[str, Any]) -> None:
        """
        Save all data to JSON file.

        Args:
            data: Dictionary containing all role questions

        Raises:
            RuntimeError: If file save operation fails
        """
        try:
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)

            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.debug("Saved database with %d roles", len(data))
        except (IOError, OSError) as e:
            logger.error("Failed to save database: %s", e)
            raise RuntimeError(f"Failed to save database: {str(e)}") from e


# Singleton instance - initialized at module load time
_QUESTION_REPOSITORY = QuestionRepository()


def get_question_repository() -> QuestionRepository:
    """
    Get singleton instance of QuestionRepository.

    Returns:
        QuestionRepository: Singleton instance
    """
    return _QUESTION_REPOSITORY
