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
    Get application settings instance.

    Cached to avoid re-loading settings on every request.

    Returns:
        Settings: Application settings instance
    """
    return settings


def get_api_key(app_settings: Settings = Depends(get_settings)) -> str:
    """
    Get validated Google API key from settings.

    Args:
        app_settings: Application settings (injected)

    Returns:
        str: Validated API key

    Raises:
        HTTPException: If API key is not configured
    """
    if not app_settings.google_api_key:
        raise HTTPException(
            status_code=500,
            detail="Google API key not configured"
        )
    return app_settings.google_api_key
