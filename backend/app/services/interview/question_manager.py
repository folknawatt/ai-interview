"""
Module for generating interview questions using Google Gemini API.

This module provides functionality to generate role-specific interview
questions based on job descriptions using Google's Gemini generative AI model.
"""
from pydantic import BaseModel

from app.adapters.ai.gemini_client import GeminiClient
from app.config.prompts import QUESTION_PROMPT


class Response(BaseModel):
    questions: list[str]


def gen_questions(
    gemini_api_key: str,
    role: str,
    description: str
) -> Response:
    """
    Generate questions based on a given job description.

    Args:
        gemini_api_key (str): Google Gemini API Key
        role (str): Role to generate questions against
        description (str): Job description to generate questions against

    Returns:
        Response: Generated questions

    Raises:
        ValueError: If API response parsing fails
        ConnectionError: If connection to Gemini API fails
        RuntimeError: If Gemini API returns an error
    """
    # Use centralized GeminiClient
    client = GeminiClient(api_key=gemini_api_key)

    # Prepare Prompt
    final_prompt = QUESTION_PROMPT.format(
        role=role,
        job_description=description
    )

    # Generate structured response
    return client.generate_structured(
        prompt=final_prompt,
        response_schema=Response
    )
