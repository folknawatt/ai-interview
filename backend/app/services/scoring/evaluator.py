"""
AI-powered interview answer evaluation module.

This module provides functionality to evaluate candidate interview answers using
Google's Gemini AI model. It scores candidates on communication, relevance, and
quality, providing structured feedback and pass/fail predictions.
"""
from app.adapters.ai.gemini_client import GeminiClient
from app.config.prompts import SYSTEM_PROMPT
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

    # Use centralized GeminiClient
    client = GeminiClient(api_key=api_key)

    # Prepare Prompt
    formatted_prompt = SYSTEM_PROMPT.format(
        role=role, question=question, answer=transcript)

    # Generate structured response
    return client.generate_structured(
        prompt=formatted_prompt,
        response_schema=InterviewEvaluationResponse
    )
