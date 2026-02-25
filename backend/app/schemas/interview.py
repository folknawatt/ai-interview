"""Interview-related Pydantic schemas.

Schemas for interview endpoints including:
- Analysis requests
- TTS requests
- Evaluation responses
"""

from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    """Text-to-speech generation request."""

    text: str = Field(..., min_length=1, max_length=5000, description="Text to convert to speech")
    provider: str = Field(
        default="vachana", pattern="^(gemini|vachana)$", description="TTS provider"
    )


class AnalysisRequest(BaseModel):
    """Interview answer analysis request."""

    transcript: str = Field(..., min_length=1, description="Interview answer transcript")
    question: str = Field(..., min_length=1, description="Interview question")


class Scores(BaseModel):
    """Score model with validation for 1-5 range."""

    communication: float = Field(ge=1.0, le=5.0, description="Communication score 1-5")
    relevance: float = Field(ge=1.0, le=5.0, description="Relevance score 1-5")
    logical_thinking: float = Field(ge=1.0, le=5.0, description="Logical thinking score 1-5")


class Feedback(BaseModel):
    """Feedback model."""

    strengths: str
    weaknesses: str
    summary: str


class InterviewEvaluationResponse(BaseModel):
    """Complete interview evaluation response."""

    reasoning: str
    scores: Scores
    feedback: Feedback
    pass_prediction: bool


# ===== Response Schemas for Interview Endpoints =====


class UploadPDFResponse(BaseModel):
    """Response for PDF upload and session creation."""

    session_id: str = Field(..., description="Created interview session ID")
    role_id: str = Field(..., description="Base role ID")
    questions: list[str] = Field(..., description="Combined list of questions")


class QuestionResponse(BaseModel):
    """Response for getting interview question."""

    status: str = Field(..., description="'continue' or 'completed'")
    question: str | None = Field(None, description="Question text")
    question_id: int | None = Field(None, description="Question ID")
    index: int | None = Field(None, description="Current question index")
    total: int | None = Field(None, description="Total number of questions")
    audio_path: str | None = Field(None, description="Path to TTS audio file")


class InterviewSummaryResponse(BaseModel):
    """Response for interview summary."""

    session_id: str = Field(..., description="Interview session ID")
    status: str = Field(..., description="Interview status")
    candidate_name: str | None = Field(None, description="Candidate name")
    role_name: str | None = Field(None, description="Role name")
    total_questions: int = Field(..., description="Total questions answered")
    aggregated_scores: Scores | None = Field(None, description="Aggregated scores")
    feedback: str | None = Field(None, description="Overall feedback")
