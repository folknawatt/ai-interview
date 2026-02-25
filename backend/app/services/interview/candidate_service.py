"""Candidate Service.

Encapsulates business logic for candidate management.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database.models import Candidate
from app.exceptions import NotFoundError


class CandidateService:
    """Service class for handling candidate management business logic."""

    @staticmethod
    async def get_or_create(session: AsyncSession, name: str, email: str | None) -> Candidate:
        """Get existing candidate or create new one.

        Args:
            session: Async Database session
            name: Candidate name
            email: Candidate email (optional)

        Returns:
            Candidate object
        """
        # If email is provided, use it for deduplication
        if email:
            result = await session.exec(select(Candidate).where(Candidate.email == email))
            candidate = result.first()
            if candidate:
                return candidate

        # Create new candidate
        candidate = Candidate(name=name, email=email)
        session.add(candidate)
        await session.commit()
        await session.refresh(candidate)

        return candidate

    @staticmethod
    async def get_by_id(session: AsyncSession, candidate_id: int) -> Candidate:
        """Retrieve candidate by ID."""
        result = await session.exec(select(Candidate).where(Candidate.id == candidate_id))
        candidate = result.first()
        if not candidate:
            raise NotFoundError(f"Candidate {candidate_id} not found")
        return candidate
