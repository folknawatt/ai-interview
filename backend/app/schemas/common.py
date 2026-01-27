"""
# pylint: disable=too-few-public-methods
Common/shared Pydantic schemas.

Shared schemas used across multiple endpoints:
- Candidate information
- Question results
- Aggregated scores
- Reports
"""
from typing import List
from pydantic import BaseModel


class CandidateInfo(BaseModel):
    """Candidate information response."""

    id: int
    name: str
    email: str | None
    session_id: str
    role_id: str
    interview_date: str
    completed: bool

    class Config:
        """Pydantic config."""

        from_attributes = True


class QuestionResultResponse(BaseModel):
    """Individual question result response."""

    id: int
    question: str
    transcript: str | None
    video_url: str | None
    communication_score: float
    relevance_score: float
    logical_thinking_score: float
    average_score: float
    feedback: dict
    pass_prediction: bool

    class Config:
        """Pydantic config."""

        from_attributes = True


class AggregatedScoreResponse(BaseModel):
    """Aggregated score response."""

    average_score: float
    communication_avg: float
    relevance_avg: float
    logical_thinking_avg: float
    pass_rate: float
    overall_recommendation: str
    questions_answered: int
    total_questions: int

    class Config:
        """Pydantic config."""

        from_attributes = True


class InterviewReportResponse(BaseModel):
    """Complete interview report with candidate, questions, and aggregated score."""

    candidate: CandidateInfo
    questions: List[QuestionResultResponse]
    aggregated_score: AggregatedScoreResponse | None


class ReportListItem(BaseModel):
    """Summary item for reports list."""

    session_id: str
    name: str
    role_id: str
    interview_date: str
    average_score: float | None
    overall_recommendation: str | None
