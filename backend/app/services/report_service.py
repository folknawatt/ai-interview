"""
Report Service.

Encapsulates business logic for report generation and statistics, including:
- Interview report listing with filtering
- Detailed report retrieval
- PDF report generation
- Overall statistics calculation
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.models import Candidate, QuestionResult, AggregatedScore
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
    def get_all_reports(
        session: Session,
        role_id: Optional[str] = None,
        min_score: Optional[float] = None,
        recommendation: Optional[str] = None
    ) -> List[ReportListItem]:
        """
        List all completed interviews with optional filtering.

        Args:
            session: Database session
            role_id: Filter by role ID
            min_score: Minimum total score
            recommendation: Filter by recommendation

        Returns:
            List of report summaries
        """
        # Base query for completed interviews
        query = session.query(
            Candidate.session_id,
            Candidate.name,
            Candidate.role_id,
            Candidate.interview_date,
            AggregatedScore.total_score,
            AggregatedScore.overall_recommendation
        ).outerjoin(
            AggregatedScore,
            Candidate.id == AggregatedScore.candidate_id
        )

        # Apply filters
        if role_id:
            query = query.filter(Candidate.role_id == role_id)

        if min_score is not None:
            query = query.filter(AggregatedScore.total_score >= min_score)

        if recommendation:
            query = query.filter(
                AggregatedScore.overall_recommendation == recommendation
            )

        results = query.order_by(Candidate.interview_date.desc()).all()

        return [
            ReportListItem(
                session_id=r.session_id,
                name=r.name,
                role_id=r.role_id,
                interview_date=r.interview_date.isoformat(),
                total_score=r.total_score,
                overall_recommendation=r.overall_recommendation
            )
            for r in results
        ]

    @staticmethod
    def get_report_details(
        session: Session,
        session_id: str
    ) -> InterviewReportResponse:
        """
        Get detailed report for a specific interview session.

        Args:
            session: Database session
            session_id: Unique session identifier

        Returns:
            Detailed interview report

        Raises:
            NotFoundError: If session not found
        """
        # Get candidate
        candidate = session.query(Candidate).filter(
            Candidate.session_id == session_id
        ).first()

        if not candidate:
            raise NotFoundError("Interview session not found")

        # Get question results
        question_results = session.query(QuestionResult).filter(
            QuestionResult.candidate_id == candidate.id
        ).order_by(QuestionResult.id).all()

        # Get aggregated score
        aggregated_score = session.query(AggregatedScore).filter(
            AggregatedScore.candidate_id == candidate.id
        ).first()

        # Convert to response models
        candidate_info = CandidateInfo(
            id=candidate.id,
            name=candidate.name,
            email=candidate.email,
            session_id=candidate.session_id,
            role_id=candidate.role_id,
            interview_date=candidate.interview_date.isoformat(),
            completed=candidate.completed
        )

        questions = [
            QuestionResultResponse(
                id=qr.id,
                question=qr.question,
                transcript=qr.transcript,
                communication_score=qr.communication_score,
                relevance_score=qr.relevance_score,
                quality_score=qr.quality_score,
                total_score=qr.total_score,
                feedback=qr.feedback,
                pass_prediction=qr.pass_prediction
            )
            for qr in question_results
        ]

        aggregated_response = None
        if aggregated_score:
            aggregated_response = AggregatedScoreResponse(
                total_score=aggregated_score.total_score,
                communication_avg=aggregated_score.communication_avg,
                relevance_avg=aggregated_score.relevance_avg,
                quality_avg=aggregated_score.quality_avg,
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
    def generate_pdf_report(
        session: Session,
        session_id: str
    ) -> bytes:
        """
        Generate PDF report for an interview.

        Args:
            session: Database session
            session_id: Unique session identifier

        Returns:
            PDF file as bytes

        Raises:
            NotFoundError: If session not found
        """

        # Get report data
        report = ReportService.get_report_details(session, session_id)

        # Generate PDF
        pdf_buffer = generate_pdf_report(report)

        return pdf_buffer

    @staticmethod
    def get_statistics(session: Session) -> Dict[str, Any]:
        """
        Get overall statistics for all completed interviews.

        Args:
            session: Database session

        Returns:
            Dictionary with statistics
        """
        # Total candidates
        total_candidates = session.query(Candidate).filter(
            Candidate.completed.is_(True)
        ).count()

        # Average score
        avg_score = session.query(
            func.avg(AggregatedScore.total_score)
        ).scalar() or 0.0

        # Pass rate
        total_with_score = session.query(AggregatedScore).count() or 1
        passed = session.query(AggregatedScore).filter(
            AggregatedScore.overall_recommendation.in_(["Strong Pass", "Pass"])
        ).count() or 0
        pass_rate = (
            (passed / total_with_score) * 100
            if total_with_score > 0
            else 0
        )

        # Recommendation breakdown
        recommendations = session.query(
            AggregatedScore.overall_recommendation,
            func.count(AggregatedScore.id)
        ).group_by(AggregatedScore.overall_recommendation).all()

        recommendation_breakdown = {
            rec: count for rec, count in recommendations}

        return {
            "total_candidates": total_candidates,
            "average_score": round(avg_score, 2),
            "pass_rate": round(pass_rate, 2),
            "recommendation_breakdown": recommendation_breakdown
        }
