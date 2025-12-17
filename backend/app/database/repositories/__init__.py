"""
Repository pattern for data access.

This package contains repositories for:
- Question data (SQL database)
- Candidate data (SQL database)
"""
from .question_repository import QuestionRepository, get_question_repository

__all__ = [
    "QuestionRepository",
    "get_question_repository",
]
