"""
Centralized configuration for AI Interview system.

This module provides application-wide settings using Pydantic for
environment variable validation and type safety.
"""
from app.config.secret_manager import _load_secrets_from_secret_manager
import os
from pathlib import Path
from typing import List
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

# Load secrets from Google Cloud Secret Manager (if configured)
# This overrides/augments local .env variables
_load_secrets_from_secret_manager()


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
    google_api_key: str

    # Database Configuration
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "ai_interview"

    @property
    def database_url(self) -> str:
        """Construct database URL from components."""
        # Use postgresql+asyncpg for async connection
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    # TTS Configuration
    tts_provider: str = "vachana"  # TTS provider to use
    tts_max_retries: int = 2
    tts_initial_delay: int = 1
    tts_audio_dir: str = os.path.join("storage", "audio")

    tts_vachana_voice: str = "th_f_1"  # Vachana voice name
    voices_dir: str = "voices"

    # Storage Configuration
    questions_file_path: str = os.path.join(
        os.path.dirname(__file__), "questions_db.json")

    # Use 'storage' at project root (or CWD in backend)
    base_storage_dir: str = "storage"

    @property
    def temp_storage_dir(self) -> str:
        """Get temporary storage directory path."""
        return os.path.join(self.base_storage_dir, "temp")

    # CORS Configuration
    cors_origins: str = "http://localhost:3000"

    # Gemini AI Configuration
    gemini_model: str = "gemini-2.5-flash"
    gemini_temperature: float = 0.2

    # JWT Authentication
    jwt_secret_key: str = "change-this-secret-key-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 24  # 24 hours
    jwt_refresh_token_expire_days: int = 7

    # Cookie Configuration
    cookie_secure: bool = False  # Set to True in production (HTTPS)
    cookie_samesite: str = "lax"
    cookie_domain: str | None = None

    # Admin Configuration
    admin_default_email: str = "admin@ai-interview.com"
    admin_default_password: str = "change-me-in-production"

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

    def validate_security(self):
        """
        Validate security settings for production readiness.
        Logs warnings if default secrets are used.
        """
        import logging
        logger = logging.getLogger("app.config.settings")

        defaults = [
            ("jwt_secret_key", "change-this-secret-key-in-production"),
            ("admin_default_password", "change-me-in-production"),
            ("postgres_password", "postgres")
        ]

        for field, unsafe_value in defaults:
            current_value = getattr(self, field)
            if current_value == unsafe_value:
                logger.warning(
                    f"SECURITY WARNING: Default value used for '{field}'. "
                    "Change this in production!"
                )


# Global settings instance
settings = Settings()
