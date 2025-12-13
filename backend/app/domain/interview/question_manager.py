"""
Module for generating interview questions using Google Gemini API.

This module provides functionality to generate role-specific interview
questions based on job descriptions using Google's Gemini generative AI model.
"""
from google import genai
from pydantic import BaseModel

from app.config.prompts import QUESTION_PROMPT
from app.config.settings import settings


class Response(BaseModel):
    questions: list[str]


def generate_questions(
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
    # Setup Google Gemini
    client = genai.Client(api_key=gemini_api_key)

    # Prepare Prompt
    final_prompt = QUESTION_PROMPT.format(
        role=role,
        job_description=description
    )

    # LLM
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=final_prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Response,
                "temperature": settings.gemini_temperature,
            })
        return response.parsed
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
