"""
Centralized configuration for AI Interview system.

This module provides application-wide settings using Pydantic for
environment variable validation and type safety.
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Pydantic automatically loads values from environment variables
    matching the field names (case-insensitive). If not found,
    it uses the default values specified here.
    """

    # Server Configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    server_url: str = "http://localhost:8000"

    # API Configuration
    google_api_key: Optional[str] = None

    # Database Configuration
    database_url: str = "postgresql://postgres:postgres@localhost:5432/ai_interview"

    # TTS Configuration
    tts_provider: str = "gemini"  # TTS provider to use: "gemini" or "edge"
    tts_max_retries: int = 2
    tts_initial_delay: int = 1
    tts_audio_dir: str = "audio"
    tts_gemini_voice: str = "kore"  # Gemini voice name
    tts_edge_voice: str = "th-TH-PremwadeeNeural"  # Edge voice name

    # Storage Configuration
    questions_file_path: str = os.path.join(
        os.path.dirname(__file__), "questions_db.json")
    temp_storage_dir: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), r"storage\temp")

    # CORS Configuration
    cors_origins: str = "http://localhost:3000"

    # Gemini AI Configuration
    gemini_model: str = "gemini-2.5-flash"
    gemini_temperature: float = 0.2

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


# Global settings instance
settings = Settings()
