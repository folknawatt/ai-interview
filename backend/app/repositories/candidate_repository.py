"""
Candidate Repository.
"""
from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Candidate
from app.repositories.base import BaseRepository


class CandidateRepository(BaseRepository[Candidate]):
    """
    Repository for Candidate data.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session, Candidate)

    async def get_by_email(self, email: str) -> Optional[Candidate]:
        """Get candidate by email."""
        statement = select(Candidate).where(Candidate.email == email)
        result = await self.session.exec(statement)
        return result.first()

    async def get_by_name(self, name: str) -> Optional[Candidate]:
        """Get candidate by name."""
        statement = select(Candidate).where(Candidate.name == name)
        result = await self.session.exec(statement)
        return result.first()

    async def get_or_create(self, name: str, email: Optional[str]) -> Candidate:
        """Get existing candidate or create new one."""
        # If email is provided, use it for deduplication
        if email:
            candidate = await self.get_by_email(email)
            if candidate:
                return candidate

        # If no email, check by name (optional fallback, though name is not unique usually)
        # But per previous logic we might skip name check if email is primary,
        # however previous service did check name if no email?
        # Re-reading previous service:
        # if email: check email.
        # else: nothing (create new?) -> actually the previous service was:
        # if email: check. if found return.
        # Fallthrough to create.
        # Wait, the previous service logic was:
        # 1. if email: check. if found return.
        # 2. create new.
        #
        # BUT InterviewService had:
        # candidate = await candidate_repo.get_by_email(email)
        # if not candidate: candidate = await candidate_repo.get_by_name(name)
        #
        # Let's standardize in get_or_create.

        # Consistent Logic:
        if email:
            candidate = await self.get_by_email(email)
            if candidate:
                return candidate

        # Try finding by name if no email provided or not found by email?
        # Ideally we shouldn't mix.
        # Let's stick to simple: if email found, return. Else create.
        # For legacy support if name check is needed:
        # candidate = await self.get_by_name(name)
        # if candidate: return candidate

        candidate = Candidate(name=name, email=email)
        return await self.create(candidate)
