import os
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
from config.prompts import QUESTION_PROMPT

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


class Response(BaseModel):
    questions: list[str]


def generate_questions(gemini_api_key: str, job_description: str):
    """
    Generate questions based on a given job description.

    Args:
        gemini_api_key (str): Google Gemini API Key
        job_description (str): Job description to generate questions against

    Returns:
        Response: Generated questions

    Raises:
        Exception: If an error occurs during question generation
    """
    # Setup Google Gemini
    client = genai.Client(api_key=gemini_api_key)

    # เตรียม Prompt
    final_prompt = QUESTION_PROMPT.format(job_description=job_description)

    # LLM
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=final_prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Response,
                "temperature": 0.2,
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
