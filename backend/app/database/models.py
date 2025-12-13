"""
SQLAlchemy ORM models for AI Interview persistent storage.

This module defines the database schema for storing interview data:
- Candidate: Information about interview candidates
- QuestionResult: Individual question answers and AI evaluations
- AggregatedScore: Computed aggregate scores and recommendations
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship

from .db import Base


class Candidate(Base):
    """
    Candidate table storing interview participant information.

    Attributes:
        id: Primary key
        name: Candidate's full name
        email: Candidate's email (optional)
        session_id: Unique session identifier for the interview
        role_id: ID of the role being interviewed for
        interview_date: Timestamp when interview was created
        completed: Whether the interview has been marked as complete
    """
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    role_id = Column(String(100), nullable=False, index=True)
    interview_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)

    # Relationships
    question_results = relationship(
        "QuestionResult",
        back_populates="candidate",
        cascade="all, delete-orphan"
    )
    aggregated_score = relationship(
        "AggregatedScore",
        back_populates="candidate",
        uselist=False,
        cascade="all, delete-orphan"
    )


class QuestionResult(Base):
    """
    QuestionResult table storing individual question evaluations.

    Attributes:
        id: Primary key
        candidate_id: Foreign key to candidate
        question: The interview question text
        transcript: Transcribed answer from candidate
        communication_score: Score for communication skills (1-10)
        relevance_score: Score for answer relevance (1-10)
        quality_score: Score for answer quality (1-10)
        total_score: Total score for this question (1-10)
        feedback: JSON object containing strengths, weaknesses, summary
        pass_prediction: AI prediction whether this answer passes
    """
    __tablename__ = "question_results"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False,
        index=True
    )
    question = Column(Text, nullable=False)
    transcript = Column(Text, nullable=True)

    # Scores (1-10 scale) - Float for decimal precision
    communication_score = Column(Float, nullable=False)
    relevance_score = Column(Float, nullable=False)
    quality_score = Column(Float, nullable=False)
    total_score = Column(Float, nullable=False)

    # Feedback stored as JSON:
    # {"strengths": "...", "weaknesses": "...", "summary": "..."}
    feedback = Column(JSON, nullable=False)
    pass_prediction = Column(Boolean, nullable=False)

    # Relationship
    candidate = relationship("Candidate", back_populates="question_results")


class AggregatedScore(Base):
    """
    AggregatedScore table storing computed aggregate metrics per candidate.

    Attributes:
        id: Primary key
        candidate_id: Foreign key to candidate (unique)
        total_score: Average total score across all questions
        communication_avg: Average communication score
        relevance_avg: Average relevance score
        quality_avg: Average quality score
        pass_rate: Percentage of questions with pass prediction
        overall_recommendation: Computed recommendation (Strong Pass/Pass/Review/Fail)
        questions_answered: Number of questions answered
        total_questions: Total number of questions for this role
    """
    __tablename__ = "aggregated_scores"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        unique=True,
        nullable=False,
        index=True
    )

    # Aggregated metrics
    total_score = Column(Float, nullable=False)
    communication_avg = Column(Float, nullable=False)
    relevance_avg = Column(Float, nullable=False)
    quality_avg = Column(Float, nullable=False)
    pass_rate = Column(Float, nullable=False)  # Percentage (0-100)
    # "Strong Pass", "Pass", "Review", "Fail"
    overall_recommendation = Column(String(50), nullable=False)

    # Question counts
    questions_answered = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)

    # Relationship
    candidate = relationship("Candidate", back_populates="aggregated_score")
