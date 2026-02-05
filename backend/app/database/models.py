"""
SQLModel models for AI Interview persistent storage.

This module defines the database schema for storing interview data:
- JobRole: Available job positions
- Question: Interview questions for each role
- Candidate: Candidate profile information
- InterviewSession: Specific interview instance linking candidate and role
- QuestionResult: Individual question answers and AI evaluations
- AggregatedScore: Computed aggregate scores and recommendations
"""
import enum
from datetime import datetime, timezone
from typing import List, Optional, Any, Dict
from sqlmodel import Field, Relationship, SQLModel, JSON
from sqlalchemy import Text


def utc_now():
    """Return current naive UTC timestamp."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class InterviewStatus(str, enum.Enum):
    """Status of an interview session."""
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class UserRole(str, enum.Enum):
    """Role for HR system users."""
    ADMIN = "admin"
    HR = "hr"
    VIEWER = "viewer"


class HRUser(SQLModel, table=True):
    """HR System User for authentication."""
    __tablename__ = "hr_users"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(max_length=100, unique=True,
                          index=True, nullable=False)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    full_name: str = Field(max_length=255, nullable=False)
    role: UserRole = Field(default=UserRole.HR, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(
        default_factory=utc_now, nullable=False)
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column_kwargs={"onupdate": utc_now},
        nullable=False
    )


class JobRole(SQLModel, table=True):
    """
    Job Role definition.
    """
    __tablename__ = "job_roles"

    id: str = Field(primary_key=True, index=True, max_length=100)
    title: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(
        default_factory=utc_now)

    # Relationships
    questions: List["Question"] = Relationship(
        back_populates="role", cascade_delete=True
    )
    sessions: List["InterviewSession"] = Relationship(back_populates="role")


class Question(SQLModel, table=True):
    """
    Interview Question.
    """
    __tablename__ = "questions"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    role_id: str = Field(
        foreign_key="job_roles.id",
        nullable=False,
        index=True,
        max_length=100
    )
    content: str = Field(sa_type=Text, nullable=False)
    order: int = Field(default=0, nullable=False)
    created_at: datetime = Field(
        default_factory=utc_now)

    # Relationships
    role: "JobRole" = Relationship(back_populates="questions")
    results: List["QuestionResult"] = Relationship(
        back_populates="question_def")


class Candidate(SQLModel, table=True):
    """
    Candidate profile.
    """
    __tablename__ = "candidates"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=255, nullable=False)
    email: Optional[str] = Field(
        default=None, max_length=255, nullable=True, index=True)
    created_at: datetime = Field(
        default_factory=utc_now, nullable=False)
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column_kwargs={"onupdate": utc_now},
        nullable=False
    )

    # Relationships
    sessions: List["InterviewSession"] = Relationship(
        back_populates="candidate",
        cascade_delete=True
    )


class InterviewSession(SQLModel, table=True):
    """
    Specific interview instance.
    """
    __tablename__ = "interview_sessions"

    session_id: str = Field(
        primary_key=True,
        index=True,
        max_length=100
    )
    candidate_id: int = Field(
        foreign_key="candidates.id",
        nullable=False,
        index=True
    )
    role_id: str = Field(
        foreign_key="job_roles.id",
        nullable=False,
        index=True,
        max_length=100
    )

    status: InterviewStatus = Field(
        default=InterviewStatus.STARTED, nullable=False)
    started_at: datetime = Field(
        default_factory=utc_now, nullable=False)
    completed_at: Optional[datetime] = Field(default=None, nullable=True)

    # Relationships
    candidate: "Candidate" = Relationship(back_populates="sessions")
    role: "JobRole" = Relationship(back_populates="sessions")

    question_results: List["QuestionResult"] = Relationship(
        back_populates="session",
        cascade_delete=True
    )
    aggregated_score: Optional["AggregatedScore"] = Relationship(
        back_populates="session",
        sa_relationship_kwargs={
            "uselist": False,
            "cascade": "all, delete-orphan"
        }
    )


class QuestionResult(SQLModel, table=True):
    """
    QuestionResult table storing individual question evaluations.
    """
    __tablename__ = "question_results"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    session_id: str = Field(
        foreign_key="interview_sessions.session_id",
        nullable=False,
        index=True,
        max_length=100
    )
    question_id: Optional[int] = Field(
        default=None, foreign_key="questions.id", nullable=True)

    question: str = Field(sa_type=Text, nullable=False)  # Snapshot of text
    transcript: Optional[str] = Field(
        default=None, sa_type=Text, nullable=True)
    video_url: Optional[str] = Field(default=None, nullable=True)

    # Scores (1-5 scale)
    communication_score: float = Field(nullable=False)
    relevance_score: float = Field(nullable=False)
    logical_thinking_score: float = Field(nullable=False)

    # Feedback stored as JSON
    feedback: Dict[str, Any] = Field(default={}, sa_type=JSON)
    pass_prediction: bool = Field(nullable=False)

    # Timestamps
    created_at: datetime = Field(
        default_factory=utc_now, nullable=False)
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column_kwargs={"onupdate": utc_now},
        nullable=False
    )

    # Relationship
    session: "InterviewSession" = Relationship(
        back_populates="question_results")
    question_def: Optional["Question"] = Relationship(back_populates="results")


class AggregatedScore(SQLModel, table=True):
    """
    AggregatedScore table storing computed aggregate metrics per session.
    """
    __tablename__ = "aggregated_scores"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    session_id: str = Field(
        foreign_key="interview_sessions.session_id",
        sa_column_kwargs={"unique": True},
        nullable=False,
        index=True,
        max_length=100
    )

    # Aggregated metrics
    average_score: float = Field(nullable=False)
    communication_avg: float = Field(nullable=False)
    relevance_avg: float = Field(nullable=False)
    logical_thinking_avg: float = Field(nullable=False)
    pass_rate: float = Field(nullable=False)  # Percentage (0-100)

    # "Strong Pass", "Pass", "Review", "Fail"
    overall_recommendation: str = Field(max_length=50, nullable=False)

    # Question counts
    questions_answered: int = Field(nullable=False)
    total_questions: int = Field(nullable=False)

    # Relationship
    session: "InterviewSession" = Relationship(
        back_populates="aggregated_score")
