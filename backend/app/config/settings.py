"""
Centralized configuration for AI Interview system.

This module provides application-wide settings using Pydantic for
environment variable validation and type safety.
"""
import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Robustly find and load .env file
env_path = Path(".env")
if not env_path.exists():
    # Attempt to find it in backend directory if running from root
    env_path = Path("backend/.env")

if not env_path.exists():
    # Attempt to find it relative to this file (backend/app/config/settings.py)
    env_path = Path(__file__).resolve().parents[2] / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()


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
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")

    # Database Configuration
    database_url: str = "postgresql://postgres:postgres@localhost:5433/ai_interview"

    # TTS Configuration
    tts_provider: str = "edge"  # TTS provider to use: "gemini" or "edge"
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
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
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
