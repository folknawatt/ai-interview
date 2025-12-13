"""
Evaluation domain models.

Pure domain models for interview answer evaluation.
These represent the core business concept of evaluating a candidate's answer.
"""
from dataclasses import dataclass


@dataclass
class Score:
    """
    Score value object representing evaluation scores on a 1-10 scale.

    Attributes:
        communication: Score for communication skills (1-10)
        relevance: Score for answer relevance to question (1-10)
        quality: Score for answer quality and depth (1-10)
        total: Total/average score (1-10)
    """

    communication: float
    relevance: float
    quality: float
    total: float

    def __post_init__(self):
        """Validate score ranges."""
        for field_name in ['communication', 'relevance', 'quality', 'total']:
            value = getattr(self, field_name)
            if not 1.0 <= value <= 10.0:
                raise ValueError(
                    f"{field_name} score must be between 1.0 and 10.0, "
                    f"got {value}"
                )


@dataclass
class Feedback:
    """
    Feedback value object containing evaluation feedback.

    Attributes:
        strengths: Positive aspects of the answer
        weaknesses: Areas for improvement
        summary: Overall evaluation summary
    """

    strengths: str
    weaknesses: str
    summary: str


@dataclass
class Evaluation:
    """
    Domain model representing a complete interview answer evaluation.

    This is the core business entity for evaluation results,
    independent of how it's stored (database) or transmitted (API).

    Attributes:
        scores: Evaluation scores
        feedback: Detailed feedback
        pass_prediction: Whether the answer is predicted to pass
    """

    scores: Score
    feedback: Feedback
    pass_prediction: bool
