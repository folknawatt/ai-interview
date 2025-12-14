"""
Mappers for converting between Domain models, ORM models, and Dictionaries.

This module provides the InterviewMapper class which handles the transformation
of data structures used throughout the application, ensuring separation of concerns
between the data layer, domain logic, and API responses.
"""
from typing import Dict, Any
from app.database.models import QuestionResult
from app.domain.models import (
    QuestionResult as DomainQuestionResult,
    Evaluation,
    Score,
    Feedback
)


class InterviewMapper:
    """Mapper for converting between Domain models, ORM models, and Dictionaries."""

    @staticmethod
    def to_orm_question_result(
        candidate_id: int,
        question: str,
        transcript: str,
        evaluation: Evaluation
    ) -> QuestionResult:
        """Convert Domain Evaluation to ORM QuestionResult."""
        return QuestionResult(
            candidate_id=candidate_id,
            question=question,
            transcript=transcript,
            communication_score=evaluation.scores.communication,
            relevance_score=evaluation.scores.relevance,
            quality_score=evaluation.scores.quality,
            total_score=evaluation.scores.total,
            feedback={
                "strengths": evaluation.feedback.strengths,
                "weaknesses": evaluation.feedback.weaknesses,
                "summary": evaluation.feedback.summary
            },
            pass_prediction=evaluation.pass_prediction
        )

    @staticmethod
    def to_domain_question_result(orm_qr: QuestionResult) -> DomainQuestionResult:
        """Convert ORM QuestionResult to Domain QuestionResult."""
        return DomainQuestionResult(
            question=orm_qr.question,
            transcript=orm_qr.transcript,
            evaluation=Evaluation(
                scores=Score(
                    communication=orm_qr.communication_score,
                    relevance=orm_qr.relevance_score,
                    quality=orm_qr.quality_score,
                    total=orm_qr.total_score
                ),
                feedback=Feedback(
                    strengths=orm_qr.feedback.get("strengths", ""),
                    weaknesses=orm_qr.feedback.get("weaknesses", ""),
                    summary=orm_qr.feedback.get("summary", "")
                ),
                pass_prediction=orm_qr.pass_prediction
            )
        )

    @staticmethod
    def to_dict(qr: QuestionResult) -> Dict[str, Any]:
        """Convert ORM QuestionResult to dictionary response format."""
        return {
            "question": qr.question,
            "transcript": qr.transcript,
            "evaluation": {
                "scores": {
                    "communication": qr.communication_score,
                    "relevance": qr.relevance_score,
                    "quality": qr.quality_score,
                    "total": qr.total_score
                },
                "feedback": qr.feedback,
                "pass_prediction": qr.pass_prediction
            }
        }
