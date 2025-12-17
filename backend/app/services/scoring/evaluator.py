"""
AI-powered interview answer evaluation module.

This module provides functionality to evaluate candidate interview answers using
Google's Gemini AI model. It scores candidates on communication, relevance, and
quality, providing structured feedback and pass/fail predictions.
"""
from google import genai

from app.config.prompts import SYSTEM_PROMPT
from app.config.settings import settings
from app.schemas.interview import InterviewEvaluationResponse


def evaluate_candidate(
    api_key: str,
    question: str,
    transcript: str | None,
    role: str
) -> InterviewEvaluationResponse:
    """
    Evaluate a candidate's transcript based on a given question.

    Args:
        api_key (str): Google API Key
        question (str): Question to evaluate the transcript against
        transcript (str | None): Transcript to evaluate
        role (str): The job role/title being interviewed for

    Returns:
        InterviewEvaluationResponse: Schema with scores, feedback, and pass prediction

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
    formatted_prompt = SYSTEM_PROMPT.format(
        role=role, question=question, answer=transcript)

    # LLM
    try:
        llm_generation_response = client.models.generate_content(
            model=settings.gemini_model,
            contents=formatted_prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": InterviewEvaluationResponse,
                "temperature": settings.gemini_temperature,
            })

        parsed_evaluation = llm_generation_response.parsed

        return parsed_evaluation

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
