"""Interview Repository."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database.models import AggregatedScore, InterviewSession, QuestionResult
from app.repositories.base import BaseRepository


class InterviewRepository(BaseRepository[InterviewSession]):
    """Repository for Interview Session and related data (QuestionResult, AggregatedScore)."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, InterviewSession)

    async def get_by_session_id(self, session_id: str) -> InterviewSession | None:
        """Get interview session by session_id string."""
        statement = select(InterviewSession).where(InterviewSession.session_id == session_id)
        result = await self.session.exec(statement)
        return result.first()

    async def get_question_results(self, session_id: str) -> list[QuestionResult]:
        """Get all question results for a session."""
        statement = select(QuestionResult).where(QuestionResult.session_id == session_id)
        result = await self.session.exec(statement)
        return result.all()

    async def get_question_result(self, session_id: str, question: str) -> QuestionResult | None:
        """Get a specific question result by session_id and question text."""
        statement = (
            select(QuestionResult)
            .where(QuestionResult.session_id == session_id)
            .where(QuestionResult.question == question)
        )
        result = await self.session.exec(statement)
        return result.first()

    async def get_question_result_by_index(
        self, session_id: str, index: int
    ) -> QuestionResult | None:
        """Get a specific question result by session_id and index (order).
        Assuming the order is preserved by creation id or we might need an 'order' field in QuestionResult later.
        For now, we fetch all and index into the list, or rely on QuestionResult id if inserted sequentially.
        Ideally QuestionResult should have an order/index field.
        However, based on current logic, we can fetch all and get by index.
        """
        results = await self.get_question_results(session_id)
        if 0 <= index < len(results):
            return results[index]
        return None

    async def save_question_result(self, question_result: QuestionResult) -> QuestionResult:
        """Save or update a question result."""
        self.session.add(question_result)
        await self.session.commit()
        await self.session.refresh(question_result)
        return question_result

    async def get_aggregated_score(self, session_id: str) -> AggregatedScore | None:
        """Get aggregated score for a session."""
        statement = select(AggregatedScore).where(AggregatedScore.session_id == session_id)
        result = await self.session.exec(statement)
        return result.first()

    async def save_aggregated_score(self, aggregated_score: AggregatedScore) -> AggregatedScore:
        """Save or update aggregated score."""
        self.session.add(aggregated_score)
        await self.session.commit()
        await self.session.refresh(aggregated_score)
        return aggregated_score

    async def get_session_questions_ordered(self, session_id: str) -> list[QuestionResult]:
        """Get all questions for a session ordered by ID."""
        statement = (
            select(QuestionResult)
            .where(QuestionResult.session_id == session_id)
            .order_by(QuestionResult.id)
        )
        result = await self.session.exec(statement)
        return result.all()
