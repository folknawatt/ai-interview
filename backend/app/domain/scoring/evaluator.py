"""
AI-powered interview answer evaluation module.

This module provides functionality to evaluate candidate interview answers using
Google's Gemini AI model. It scores candidates on communication, relevance, and
quality, providing structured feedback and pass/fail predictions.
"""
from google import genai
from pydantic import BaseModel, Field

from app.config.prompts import SYSTEM_PROMPT
from app.config.settings import settings
from app.domain.models import Evaluation, Feedback, Score


# Pydantic schemas for Gemini API (infrastructure concern)
class ScoresSchema(BaseModel):
    """Score schema for Gemini API response."""

    communication: float = Field(ge=1.0, le=10.0)
    relevance: float = Field(ge=1.0, le=10.0)
    quality: float = Field(ge=1.0, le=10.0)
    total: float = Field(ge=1.0, le=10.0)


class FeedbackSchema(BaseModel):
    """Feedback schema for Gemini API response."""

    strengths: str
    weaknesses: str
    summary: str


class InterviewEvaluationResponseSchema(BaseModel):
    """Complete interview evaluation response schema for Gemini API."""

    scores: ScoresSchema
    feedback: FeedbackSchema
    pass_prediction: bool


def evaluate_candidate(
    api_key: str,
    question: str,
    transcript: str | None
) -> Evaluation:
    """
    Evaluate a candidate's transcript based on a given question.

    Args:
        api_key (str): Google API Key
        question (str): Question to evaluate the transcript against
        transcript (str | None): Transcript to evaluate

    Returns:
        Evaluation: Domain model with scores, feedback, and pass prediction

    Raises:
        ValueError: If transcript is empty/None or API response parsing fails
        ConnectionError: If connection to Gemini API fails
        RuntimeError: If Gemini API returns an error
    """
    # Validate transcript is not empty
    if not transcript or transcript.strip() == "":
        raise ValueError(
            "Transcript is empty or None. Cannot evaluate empty answer."
        )

    # Validate transcript is not an error message
    error_patterns = [
        "Transcription failed",
        "Transcription unavailable",
        "Error:",
        "failed to",
        "not installed"
    ]

    transcript_lower = transcript.lower()
    for pattern in error_patterns:
        if pattern.lower() in transcript_lower:
            raise ValueError(
                f"Transcript appears to be an error message: {transcript[:100]}"
            )

    # Setup Google Gemini
    client = genai.Client(api_key=api_key)

    # Prepare Prompt
    final_prompt = SYSTEM_PROMPT.format(question=question, answer=transcript)

    # LLM
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=final_prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": InterviewEvaluationResponseSchema,
                "temperature": settings.gemini_temperature,
            })

        api_response = response.parsed

        # Post-validation: Ensure total score equals average
        calculated_total = round(
            (
                api_response.scores.communication +
                api_response.scores.relevance +
                api_response.scores.quality
            ) / 3,
            1
        )

        # Override if AI calculated incorrectly (tolerance 0.1)
        if abs(api_response.scores.total - calculated_total) > 0.1:
            api_response.scores.total = calculated_total

        # Convert Pydantic schema to domain model
        return Evaluation(
            scores=Score(
                communication=api_response.scores.communication,
                relevance=api_response.scores.relevance,
                quality=api_response.scores.quality,
                total=api_response.scores.total
            ),
            feedback=Feedback(
                strengths=api_response.feedback.strengths,
                weaknesses=api_response.feedback.weaknesses,
                summary=api_response.feedback.summary
            ),
            pass_prediction=api_response.pass_prediction
        )
    except ValueError as e:
        # Handle validation or parsing errors
        raise ValueError(f"Failed to parse API response: {str(e)}") from e
    except ConnectionError as e:
        # Handle network/connection errors
        raise ConnectionError(
            f"Failed to connect to Gemini API: {str(e)}") from e
    except RuntimeError as e:
        # Handle API-specific runtime errors
        raise RuntimeError(f"Gemini API error: {str(e)}") from e
