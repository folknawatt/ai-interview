"""
Report Service.

Encapsulates business logic for report generation and statistics, including:
- Interview report listing with filtering
- Detailed report retrieval
- PDF report generation
- Overall statistics calculation
"""
from typing import Optional, List, Dict, Any
from sqlmodel import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import (
    Candidate,
    InterviewSession,
    QuestionResult,
    AggregatedScore
)
from app.exceptions import NotFoundError
from app.schemas import (
    ReportListItem,
    InterviewReportResponse,
    CandidateInfo,
    QuestionResultResponse,
    AggregatedScoreResponse
)
from app.adapters.pdf.report_generator import generate_pdf_report


class ReportService:
    """Service class for handling report generation business logic."""

    @staticmethod
    async def get_all_reports(
        session: AsyncSession,
        role_id: Optional[str] = None,
        min_score: Optional[float] = None,
        recommendation: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[ReportListItem]:
        """
        List all completed interviews with optional filtering.

        Args:
            session: Async Database session
            role_id: Filter by role ID
            min_score: Minimum total score
            recommendation: Filter by recommendation

        Returns:
            List of report summaries
        """
        # SQLModel select tuple:
        statement = (
            select(
                InterviewSession.session_id,
                Candidate.name,
                InterviewSession.role_id,
                InterviewSession.started_at,
                AggregatedScore.average_score,
                AggregatedScore.overall_recommendation
            )
            .join(Candidate, InterviewSession.candidate_id == Candidate.id)
            .outerjoin(AggregatedScore, InterviewSession.session_id == AggregatedScore.session_id)
        )

        if role_id:
            statement = statement.where(InterviewSession.role_id == role_id)

        if min_score is not None:
            statement = statement.where(
                AggregatedScore.average_score >= min_score)

        if recommendation:
            statement = statement.where(
                AggregatedScore.overall_recommendation == recommendation
            )

        if search_query:
            statement = statement.where(
                # pylint: disable=no-member
                Candidate.name.contains(search_query)
            )

        # Ordering
        statement = statement.order_by(desc(InterviewSession.started_at))

        result = await session.exec(statement)
        results = result.all()

        return [
            ReportListItem(
                session_id=r[0],
                name=r[1],
                role_id=r[2],
                interview_date=r[3].isoformat() if hasattr(r[3], 'isoformat') else str(
                    r[3]),
                average_score=r[4] if r[4] is not None else 0.0,
                overall_recommendation=r[5] if r[5] else "Pending"
            )
            for r in results
        ]

    @staticmethod
    async def get_report_details(
        session: AsyncSession,
        session_id: str
    ) -> InterviewReportResponse:
        """
        Get detailed report for a specific interview session.
        """
        # Get session
        result_sess = await session.exec(
            select(InterviewSession).where(
                InterviewSession.session_id == session_id)
        )
        interview_sess = result_sess.first()

        if not interview_sess:
            raise NotFoundError("Interview session not found")

        # Get candidate via relationship (Async Loading)
        # Since AsyncSession doesn't support lazy loading attributes directly unless configured,
        # we often need to fetch it explicitly or ensure it's loaded.
        # However, for simple FK relationships, we can fetch Candidate by ID.
        result_candidate = await session.exec(
            select(Candidate).where(
                Candidate.id == interview_sess.candidate_id)
        )
        candidate = result_candidate.one()

        # Get question results
        result_qr = await session.exec(
            select(QuestionResult)
            .where(QuestionResult.session_id == session_id)
            .order_by(QuestionResult.id)
        )
        question_results = result_qr.all()

        # Get aggregated score
        result_agg = await session.exec(
            select(AggregatedScore)
            .where(AggregatedScore.session_id == session_id)
        )
        aggregated_score = result_agg.first()

        # Convert to response models
        # Note: CandidateInfo expects 'completed' boolean.
        # InterviewSession has 'completed_at'.
        is_completed = interview_sess.status == "completed"

        candidate_info = CandidateInfo(
            id=candidate.id,
            name=candidate.name,
            email=candidate.email,
            session_id=interview_sess.session_id,
            role_id=interview_sess.role_id,
            interview_date=interview_sess.started_at.isoformat(),
            completed=is_completed
        )

        questions = [
            QuestionResultResponse(
                id=qr.id,
                question=qr.question,
                transcript=qr.transcript,
                communication_score=qr.communication_score,
                relevance_score=qr.relevance_score,
                logical_thinking_score=qr.logical_thinking_score,
                average_score=round(
                    (qr.communication_score + qr.relevance_score + qr.logical_thinking_score) / 3, 2),
                feedback=qr.feedback,
                pass_prediction=qr.pass_prediction,
                video_url=qr.video_url
            )
            for qr in question_results
        ]

        aggregated_response = None
        if aggregated_score:
            aggregated_response = AggregatedScoreResponse(
                average_score=aggregated_score.average_score,
                communication_avg=aggregated_score.communication_avg,
                relevance_avg=aggregated_score.relevance_avg,
                logical_thinking_avg=aggregated_score.logical_thinking_avg,
                pass_rate=aggregated_score.pass_rate,
                overall_recommendation=aggregated_score.overall_recommendation,
                questions_answered=aggregated_score.questions_answered,
                total_questions=aggregated_score.total_questions
            )

        return InterviewReportResponse(
            candidate=candidate_info,
            questions=questions,
            aggregated_score=aggregated_response
        )

    @staticmethod
    async def generate_pdf_report(
        session: AsyncSession,
        session_id: str
    ) -> bytes:
        """
        Generate PDF report for an interview.
        """
        report = await ReportService.get_report_details(session, session_id)
        # PDF generation is CPU bound, should ideally run in threadpool
        # but for now we keep it simple as it's just processing the data object
        pdf_buffer = generate_pdf_report(report)
        return pdf_buffer

    @staticmethod
    async def get_statistics(session: AsyncSession) -> Dict[str, Any]:
        """
        Get overall statistics for all completed interviews.
        """
        # Total candidates (approximated by completed sessions)
        result_total = await session.exec(
            select(func.count(InterviewSession.session_id))
            .where(InterviewSession.status == "completed")
        )
        total_candidates = result_total.one()

        # Average score
        result_avg = await session.exec(
            select(func.avg(AggregatedScore.average_score))
        )
        avg_score = result_avg.one() or 0.0

        # Pass rate
        result_total_score = await session.exec(
            select(func.count(AggregatedScore.id))
        )
        total_with_score = result_total_score.one() or 1

        result_passed = await session.exec(
            select(func.count(AggregatedScore.id))
            .where(AggregatedScore.overall_recommendation.in_(["Strong Pass", "Pass"]))  # pylint: disable=no-member
        )
        passed = result_passed.one() or 0

        pass_rate = (
            (passed / total_with_score) * 100
            if total_with_score > 0
            else 0
        )

        # Recommendation breakdown
        result_recs = await session.exec(
            select(
                AggregatedScore.overall_recommendation,
                func.count(AggregatedScore.id)
            ).group_by(AggregatedScore.overall_recommendation)
        )
        recommendations = result_recs.all()

        recommendation_breakdown = {
            rec: count for rec, count in recommendations}

        return {
            "total_candidates": total_candidates,
            "average_score": round(float(avg_score), 2),
            "pass_rate": round(pass_rate, 2),
            "recommendation_breakdown": recommendation_breakdown
        }

    # End of class
