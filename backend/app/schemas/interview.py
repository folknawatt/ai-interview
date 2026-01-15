"""
Interview-related Pydantic schemas.

Schemas for interview endpoints including:
- Analysis requests
- TTS requests
- Evaluation responses
"""
from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    """Text-to-speech generation request."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Text to convert to speech"
    )
    provider: str = Field(
        default="gemini",
        pattern="^(gemini|edge)$",
        description="TTS provider"
    )


class AnalysisRequest(BaseModel):
    """Interview answer analysis request."""

    transcript: str = Field(
        ...,
        min_length=1,
        description="Interview answer transcript"
    )
    question: str = Field(
        ...,
        min_length=1,
        description="Interview question"
    )


class Scores(BaseModel):
    """Score model with validation for 1-5 range."""

    communication: float = Field(
        ge=1.0,
        le=5.0,
        description="Communication score 1-5"
    )
    relevance: float = Field(
        ge=1.0,
        le=5.0,
        description="Relevance score 1-5"
    )
    logical_thinking: float = Field(
        ge=1.0,
        le=5.0,
        description="Logical thinking score 1-5"
    )


class Feedback(BaseModel):
    """Feedback model."""

    strengths: str
    weaknesses: str
    summary: str


class InterviewEvaluationResponse(BaseModel):
    """Complete interview evaluation response."""

    scores: Scores
    feedback: Feedback
    pass_prediction: bool
