
from typing import Optional, Type, TypeVar
from google import genai
from google.genai import types
from pydantic import BaseModel
from app.config.settings import settings

T = TypeVar('T', bound=BaseModel)


class GeminiClient:
    """Centralized client for Gemini API interactions."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize GeminiClient.

        Args:
            api_key: Optional API key. If not provided, uses settings.google_api_key.
        """
        self._api_key = api_key or settings.google_api_key
        if not self._api_key:
            raise ValueError("GOOGLE_API_KEY is not set in settings.")
        self.client = genai.Client(api_key=self._api_key)

    def generate_content(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate content using Gemini API.

        Args:
            prompt: The input prompt.
            model: Model name to use (defaults to settings).
            temperature: Temperature for generation (defaults to settings).

        Returns:
            Generated text content.
        """
        model = model or settings.gemini_model
        temperature = temperature if temperature is not None else settings.gemini_temperature

        try:
            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    response_mime_type="application/json"
                )
            )
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {str(e)}") from e

    def generate_structured(
        self,
        prompt: str,
        response_schema: Type[T],
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> T:
        """
        Generate structured content using Gemini API with schema validation.

        Args:
            prompt: The input prompt.
            response_schema: Pydantic model class for response validation.
            model: Model name to use (defaults to settings).
            temperature: Temperature for generation (defaults to settings).

        Returns:
            Parsed response matching the provided schema.

        Raises:
            ValueError: If API response parsing fails.
            ConnectionError: If connection to Gemini API fails.
            RuntimeError: If Gemini API returns an error.
        """
        model = model or settings.gemini_model
        temperature = temperature if temperature is not None else settings.gemini_temperature

        try:
            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": response_schema,
                    "temperature": temperature,
                }
            )
            return response.parsed
        except ValueError as e:
            raise ValueError(f"Failed to parse API response: {str(e)}") from e
        except ConnectionError as e:
            raise ConnectionError(
                f"Failed to connect to Gemini API: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}") from e
