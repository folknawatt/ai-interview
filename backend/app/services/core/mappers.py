"""Mappers for converting between Domain models, ORM models, and Dictionaries.

This module provides the InterviewMapper class which handles the transformation
of data structures used throughout the application, ensuring separation of concerns
between the data layer, domain logic, and API responses.
"""

from typing import Any

from app.database.models import QuestionResult
from app.schemas.interview import InterviewEvaluationResponse


class InterviewMapper:
    """Mapper for converting between Domain models, ORM models, and Dictionaries."""

    @staticmethod
    def to_orm_question_result(
        session_id: str,
        question_id: int,  # Note: This is actually question_result_id from Snapshot Pattern
        question: str,
        transcript: str,
        evaluation: InterviewEvaluationResponse,
    ) -> QuestionResult:
        """Convert Schema Evaluation to ORM QuestionResult.

        Note: question_id parameter is NOT used as FK to questions table
        since Snapshot Pattern stores questions directly in QuestionResult.question field.
        """
        return QuestionResult(
            session_id=session_id,
            # question_id FK intentionally left as None for Snapshot Pattern
            # Session questions aren't stored in the 'questions' table
            question=question,
            transcript=transcript,
            communication_score=evaluation.scores.communication,
            relevance_score=evaluation.scores.relevance,
            logical_thinking_score=evaluation.scores.logical_thinking,
            feedback={
                "strengths": evaluation.feedback.strengths,
                "weaknesses": evaluation.feedback.weaknesses,
                "summary": evaluation.feedback.summary,
                "reasoning": getattr(evaluation, "reasoning", ""),
            },
            pass_prediction=evaluation.pass_prediction,
        )

    @staticmethod
    def to_dict(qr: QuestionResult) -> dict[str, Any]:
        """Convert ORM QuestionResult to dictionary response format."""
        return {
            "question": qr.question,
            "transcript": qr.transcript,
            "evaluation": {
                "scores": {
                    "communication": qr.communication_score,
                    "relevance": qr.relevance_score,
                    "logical_thinking": qr.logical_thinking_score,
                },
                "feedback": qr.feedback,
                "pass_prediction": qr.pass_prediction,
            },
        }
