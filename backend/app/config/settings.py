"""
Centralized configuration for AI Interview system.

This module provides application-wide settings using Pydantic for
environment variable validation and type safety.
"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Pydantic automatically loads values from environment variables
    matching the field names (case-insensitive). If not found,
    it uses the default values specified here.
    """

    # API Keys (Required - no default for security)
    google_api_key: str

    # Storage Configuration
    database_file: str = "app/config/questions_db.json"
    temp_storage_dir: str = "storage/temp"

    # CORS Configuration
    cors_origins: str = "http://localhost:3000"

    # Gemini AI Configuration
    gemini_model: str = "gemini-2.5-flash"
    gemini_temperature: float = 0.2

    # Server Configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8000

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }


# Global settings instance
settings = Settings()
