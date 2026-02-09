"""
Abstract Base Repository.
"""
from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlmodel import select, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    """
    Base repository implementing common CRUD operations.
    """

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get(self, record_id: Any) -> Optional[T]:
        """Get a single record by ID."""
        return await self.session.get(self.model, record_id)

    async def get_all(self) -> List[T]:
        """Get all records."""
        statement = select(self.model)
        result = await self.session.exec(statement)
        return result.all()

    async def create(self, obj: T) -> T:
        """Create a new record."""
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: T) -> T:
        """Update an existing record."""
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: T) -> None:
        """Delete a record."""
        await self.session.delete(obj)
        await self.session.commit()
