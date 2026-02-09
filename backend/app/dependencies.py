"""
FastAPI dependency injection utilities.

Provides reusable dependencies for:
- Settings access
- API key validation
- Common configurations
"""
from functools import lru_cache
from fastapi import Depends, HTTPException
from app.config.settings import Settings, settings


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings instance.

    Returns singleton to avoid repeated environment parsing (FastAPI best practice).
    """
    return settings


def get_api_key(app_settings: Settings = Depends(get_settings)) -> str:
    """
    Get validated Google API key from settings.

    This dependency ensures the API key is configured before processing requests
    that require Gemini AI access (e.g., candidate evaluation, question generation).

    Dependency injection pattern: FastAPI auto-injects settings via Depends()

    Args:
        app_settings: Application settings (auto-injected by FastAPI)

    Returns:
        str: Google API key for Gemini services

    Raises:
        HTTPException: 500 if API key is not configured in environment
    """
    # Validate API key is present before allowing AI operations
    if not app_settings.google_api_key:
        raise HTTPException(
            status_code=500,
            detail="Google API key not configured"
        )
    return app_settings.google_api_key
