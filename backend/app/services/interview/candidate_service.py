"""
Candidate Service.

Encapsulates business logic for candidate management.
"""
from typing import Optional
from sqlmodel import Session, select

from app.database.models import Candidate
from app.exceptions import NotFoundError


class CandidateService:
    """Service class for handling candidate management business logic."""

    @staticmethod
    def get_or_create(
        session: Session,
        name: str,
        email: Optional[str]
    ) -> Candidate:
        """
        Get existing candidate or create new one.

        Args:
            session: Database session
            name: Candidate name
            email: Candidate email (optional)

        Returns:
            Candidate object
        """
        # If email is provided, use it for deduplication
        if email:
            candidate = session.exec(
                select(Candidate).where(Candidate.email == email)
            ).first()
            if candidate:
                return candidate

        # Create new candidate
        candidate = Candidate(
            name=name,
            email=email
        )
        session.add(candidate)
        session.commit()
        session.refresh(candidate)

        return candidate

    @staticmethod
    def get_by_id(session: Session, candidate_id: int) -> Candidate:
        """Retrieve candidate by ID."""
        candidate = session.exec(
            select(Candidate).where(Candidate.id == candidate_id)
        ).first()
        if not candidate:
            raise NotFoundError(f"Candidate {candidate_id} not found")
        return candidate
