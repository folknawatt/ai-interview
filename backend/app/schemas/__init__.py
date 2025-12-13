"""
Pydantic schemas package.

This package contains schemas organized by feature:
- hr.py: Schemas for HR endpoints
- interview.py: Schemas for interview endpoints
- common.py: Shared schemas
"""
from .hr import JDInput, SaveQuestionsRequest, UpdateQuestionsRequest
from .interview import (
    AnalysisRequest,
    Feedback,
    InterviewEvaluationResponse,
    Scores,
    TTSRequest,
)
from .common import (
    AggregatedScoreResponse,
    CandidateInfo,
    InterviewReportResponse,
    QuestionResultResponse,
    ReportListItem,
)

__all__ = [
    # HR schemas
    "JDInput",
    "SaveQuestionsRequest",
    "UpdateQuestionsRequest",
    # Interview schemas
    "AnalysisRequest",
    "Feedback",
    "InterviewEvaluationResponse",
    "Scores",
    "TTSRequest",
    # Common schemas
    "AggregatedScoreResponse",
    "CandidateInfo",
    "InterviewReportResponse",
    "QuestionResultResponse",
    "ReportListItem",
]
