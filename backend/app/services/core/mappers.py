"""
Mappers for converting between Domain models, ORM models, and Dictionaries.

This module provides the InterviewMapper class which handles the transformation
of data structures used throughout the application, ensuring separation of concerns
between the data layer, domain logic, and API responses.
"""
from typing import Dict, Any
from app.database.models import QuestionResult
from app.schemas.interview import InterviewEvaluationResponse


class InterviewMapper:
    """Mapper for converting between Domain models, ORM models, and Dictionaries."""

    @staticmethod
    def to_orm_question_result(
        session_id: str,
        question_id: int,
        question: str,
        transcript: str,
        evaluation: InterviewEvaluationResponse
    ) -> QuestionResult:
        """Convert Schema Evaluation to ORM QuestionResult."""
        return QuestionResult(
            session_id=session_id,
            question_id=question_id,
            question=question,
            transcript=transcript,
            communication_score=evaluation.scores.communication,
            relevance_score=evaluation.scores.relevance,
            logical_thinking_score=evaluation.scores.logical_thinking,
            feedback={
                "strengths": evaluation.feedback.strengths,
                "weaknesses": evaluation.feedback.weaknesses,
                "summary": evaluation.feedback.summary,
                "reasoning": hasattr(evaluation, 'reasoning') and evaluation.reasoning or ""
            },
            pass_prediction=evaluation.pass_prediction
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
                    "logical_thinking": qr.logical_thinking_score
                },
                "feedback": qr.feedback,
                "pass_prediction": qr.pass_prediction
            }
        }
