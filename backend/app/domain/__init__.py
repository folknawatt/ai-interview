"""
Domain package for core business logic.

This package contains:
- models: Pure domain entities (Evaluation, AggregatedScore, etc.)
- scoring: AI evaluation and aggregation logic
- interview: Question management logic
"""
# Re-export models for convenience
from .models import (  # noqa: F401
    AggregatedScore,
    Candidate,
    Evaluation,
    Feedback,
    QuestionResult,
    Score,
)

__all__ = [
    "AggregatedScore",
    "Candidate",
    "Evaluation",
    "Feedback",
    "QuestionResult",
    "Score",
]
