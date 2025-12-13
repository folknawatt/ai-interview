"""
Candidate Service.

Encapsulates business logic for candidate management, including:
- Candidate retrieval and creation
- Session management
- Interview completion tracking
"""
from sqlalchemy.orm import Session

from app.database.models import Candidate
from app.exceptions import NotFoundError


class CandidateService:
    """Service class for handling candidate management business logic."""

    @staticmethod
    def get_or_create(
        session: Session,
        session_id: str,
        name: str,
        email: str,
        role_id: str
    ) -> Candidate:
        """
        Get existing candidate or create new one.

        Args:
            session: Database session
            session_id: Unique session identifier
            name: Candidate name
            email: Candidate email
            role_id: Job role identifier

        Returns:
            Candidate object
        """
        candidate = (
            session.query(Candidate)
            .filter(Candidate.session_id == session_id)
            .first()
        )

        if not candidate:
            candidate = Candidate(
                session_id=session_id,
                name=name,
                email=email,
                role_id=role_id,
                completed=False
            )
            session.add(candidate)
            session.commit()
            session.refresh(candidate)

        return candidate

    @staticmethod
    def mark_completed(session: Session, session_id: str) -> Candidate:
        """
        Mark interview as completed for a candidate.

        Args:
            session: Database session
            session_id: Unique session identifier

        Returns:
            Updated candidate object

        Raises:
            NotFoundError: If candidate not found
        """
        candidate = (
            session.query(Candidate)
            .filter(Candidate.session_id == session_id)
            .first()
        )

        if not candidate:
            raise NotFoundError("Candidate session not found")

        candidate.completed = True
        session.commit()
        session.refresh(candidate)

        return candidate

    @staticmethod
    def get_by_session_id(session: Session, session_id: str) -> Candidate:
        """
        Retrieve candidate by session ID.

        Args:
            session: Database session
            session_id: Unique session identifier

        Returns:
            Candidate object

        Raises:
            NotFoundError: If candidate not found
        """
        candidate = (
            session.query(Candidate)
            .filter(Candidate.session_id == session_id)
            .first()
        )

        if not candidate:
            raise NotFoundError("Candidate session not found")

        return candidate
