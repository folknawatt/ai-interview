"""
SQLAlchemy ORM models for AI Interview persistent storage.

This module defines the database schema for storing interview data:
- JobRole: Available job positions
- Question: Interview questions for each role
- Candidate: Candidate profile information
- InterviewSession: Specific interview instance linking candidate and role
- QuestionResult: Individual question answers and AI evaluations
- AggregatedScore: Computed aggregate scores and recommendations
"""
import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey, Text,
    Enum
)
from sqlalchemy.orm import relationship

from .db import Base


class InterviewStatus(str, enum.Enum):
    """Status of an interview session."""
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class JobRole(Base):
    """
    Job Role definition.

    Attributes:
        id: Unique identifier (e.g., 'software-engineer')
        title: Human readable title
    """
    __tablename__ = "job_roles"

    id = Column(String(100), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    questions = relationship(
        "Question", back_populates="role", cascade="all, delete-orphan")
    sessions = relationship("InterviewSession", back_populates="role")


class Question(Base):
    """
    Interview Question.

    Attributes:
        id: Primary key
        role_id: Foreign key to JobRole
        content: The question text
        order: Sequence order
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(String(100), ForeignKey(
        "job_roles.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    role = relationship("JobRole", back_populates="questions")
    results = relationship("QuestionResult", back_populates="question_def")


class Candidate(Base):
    """
    Candidate profile.

    Attributes:
        id: Primary key
        name: Candidate's full name
        email: Candidate's email (optional)
        created_at: Timestamp when candidate was first seen
    """
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    sessions = relationship(
        "InterviewSession",
        back_populates="candidate",
        cascade="all, delete-orphan"
    )


class InterviewSession(Base):
    """
    Specific interview instance.

    Attributes:
        session_id: Unique UUID for the session (PK)
        candidate_id: FK to Candidate
        role_id: FK to JobRole
        status: Current status (started, completed, etc)
    """
    __tablename__ = "interview_sessions"

    session_id = Column(String(100), primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey(
        "candidates.id"), nullable=False, index=True)
    role_id = Column(String(100), ForeignKey(
        "job_roles.id"), nullable=False, index=True)

    status = Column(Enum(InterviewStatus),
                    default=InterviewStatus.STARTED, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    candidate = relationship("Candidate", back_populates="sessions")
    role = relationship("JobRole", back_populates="sessions")

    question_results = relationship(
        "QuestionResult",
        back_populates="session",
        cascade="all, delete-orphan"
    )
    aggregated_score = relationship(
        "AggregatedScore",
        back_populates="session",
        uselist=False,
        cascade="all, delete-orphan"
    )


class QuestionResult(Base):
    """
    QuestionResult table storing individual question evaluations.

    Attributes:
        id: Primary key
        session_id: Foreign key to interview session
        question_id: Foreign key to question definition (optional, for linkage)
        question_text: Snapshot of question text (for historical integrity)
        transcript: Transcribed answer from candidate
        communication_score: Score for communication skills (1-10)
        relevance_score: Score for answer relevance (1-10)
        logical_thinking_score: Score for logical thinking (1-10)
        total_score: Total score for this question (1-10)
        feedback: JSON object containing strengths, weaknesses, summary
        pass_prediction: AI prediction whether this answer passes
    """
    __tablename__ = "question_results"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        String(100),
        ForeignKey("interview_sessions.session_id"),
        nullable=False,
        index=True
    )
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)

    question = Column(Text, nullable=False)  # Snapshot of text
    transcript = Column(Text, nullable=True)

    # Scores (1-10 scale) - Float for decimal precision
    communication_score = Column(Float, nullable=False)
    relevance_score = Column(Float, nullable=False)
    logical_thinking_score = Column(Float, nullable=False)
    total_score = Column(Float, nullable=False)

    # Feedback stored as JSON:
    # {"strengths": "...", "weaknesses": "...", "summary": "..."}
    feedback = Column(JSON, nullable=False)
    pass_prediction = Column(Boolean, nullable=False)

    # Relationship
    session = relationship(
        "InterviewSession", back_populates="question_results")
    question_def = relationship("Question", back_populates="results")


class AggregatedScore(Base):
    """
    AggregatedScore table storing computed aggregate metrics per session.

    Attributes:
        id: Primary key
        session_id: Foreign key to interview session (unique)
        total_score: Average total score across all questions
        communication_avg: Average communication score
        relevance_avg: Average relevance score
        logical_thinking_avg: Average logical thinking score
        pass_rate: Percentage of questions with pass prediction
        overall_recommendation: Computed recommendation (Strong Pass/Pass/Review/Fail)
        questions_answered: Number of questions answered
        total_questions: Total number of questions for this role
    """
    __tablename__ = "aggregated_scores"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        String(100),
        ForeignKey("interview_sessions.session_id"),
        unique=True,
        nullable=False,
        index=True
    )

    # Aggregated metrics
    total_score = Column(Float, nullable=False)
    communication_avg = Column(Float, nullable=False)
    relevance_avg = Column(Float, nullable=False)
    logical_thinking_avg = Column(Float, nullable=False)
    pass_rate = Column(Float, nullable=False)  # Percentage (0-100)
    # "Strong Pass", "Pass", "Review", "Fail"
    overall_recommendation = Column(String(50), nullable=False)

    # Question counts
    questions_answered = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)

    # Relationship
    session = relationship(
        "InterviewSession", back_populates="aggregated_score")
