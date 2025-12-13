"""
Aggregated score domain model.

Pure domain model representing aggregated interview performance metrics.
"""
from dataclasses import dataclass


@dataclass
class AggregatedScore:
    """
    Domain model representing aggregated performance across all questions.

    This model contains computed metrics and overall recommendations
    based on all question results for a candidate.

    Attributes:
        total_score: Average total score across all questions (1-10)
        communication_avg: Average communication score (1-10)
        relevance_avg: Average relevance score (1-10)
        quality_avg: Average quality score (1-10)
        pass_rate: Percentage of questions with pass prediction (0-100)
        overall_recommendation: Overall hiring recommendation
            (Strong Pass, Pass, Review, Fail)
        questions_answered: Number of questions answered
        total_questions: Total number of questions for the role
    """

    total_score: float
    communication_avg: float
    relevance_avg: float
    quality_avg: float
    pass_rate: float
    overall_recommendation: str
    questions_answered: int
    total_questions: int

    def __post_init__(self):
        """Validate score ranges and values."""
        # Validate scores are in 1-10 range
        for field_name in [
            'total_score',
            'communication_avg',
            'relevance_avg',
            'quality_avg'
        ]:
            value = getattr(self, field_name)
            if not 0.0 <= value <= 10.0:
                raise ValueError(
                    f"{field_name} must be between 0.0 and 10.0, got {value}"
                )

        # Validate pass_rate is percentage
        if not 0.0 <= self.pass_rate <= 100.0:
            raise ValueError(
                f"pass_rate must be between 0.0 and 100.0, "
                f"got {self.pass_rate}"
            )

        # Validate recommendation
        valid_recommendations = ["Strong Pass", "Pass", "Review", "Fail"]
        if self.overall_recommendation not in valid_recommendations:
            raise ValueError(
                f"overall_recommendation must be one of {valid_recommendations}, "
                f"got '{self.overall_recommendation}'"
            )

        # Validate question counts
        if self.questions_answered < 0 or self.total_questions < 0:
            raise ValueError("Question counts cannot be negative")
        if self.questions_answered > self.total_questions:
            raise ValueError(
                "questions_answered cannot exceed total_questions"
            )
