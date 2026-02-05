"""
TTS Service for audio generation.

Handles text-to-speech generation with retry logic and error handling.
"""
import shutil
import time
from pathlib import Path
from typing import Optional

from app.adapters.tts.factory import TTSProviderFactory
from app.config.settings import settings
from app.config.logging_config import get_logger


logger = get_logger(__name__)


class TTSService:
    """Service for managing TTS generation with retry logic."""

    @staticmethod
    def generate_question_audio(
        text: str,
        question_id: int
    ) -> Optional[str]:
        """
        Generate TTS audio for a question with retry logic.

        Args:
            text: Question text to convert to speech
            question_id: Question ID for filename

        Returns:
            Absolute URL to audio file, or None if generation fails

        Raises:
            None - All exceptions are handled internally
        """
        max_retries = settings.tts_max_retries
        retry_delay = settings.tts_initial_delay

        for attempt in range(max_retries + 1):
            try:
                # Create TTS provider from settings
                provider = TTSProviderFactory.create_from_settings()

                logger.info(
                    "Using TTS provider: %s (attempt %d/%d)",
                    provider.get_provider_name(),
                    attempt + 1,
                    max_retries + 1
                )

                # Generate TTS audio using the configured provider
                temp_audio_path = provider.generate_audio(text=text)

                # Save to public directory
                return TTSService._save_audio_file(temp_audio_path, question_id)

            except (OSError, RuntimeError) as e:
                error_msg = str(e)

                # Check if it's a 503 overload error
                if "503" in error_msg or "overloaded" in error_msg.lower():
                    if attempt < max_retries:
                        logger.warning(
                            "TTS provider overloaded (attempt %d/%d). Retrying in %ss...",
                            attempt + 1, max_retries + 1, retry_delay
                        )
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        logger.error(
                            "TTS provider still overloaded after %d attempts. "
                            "Continuing without audio.",
                            max_retries + 1
                        )
                else:
                    logger.error("Failed to generate TTS: %s", error_msg)

                # Return None on final failure
                return None

        return None

    @staticmethod
    def _save_audio_file(source_path: str, question_id: int) -> str:
        """
        Helper: Copy generated audio to public static directory.
        """
        # Copy to audio directory for frontend access
        audio_dir = Path.cwd() / settings.tts_audio_dir
        audio_dir.mkdir(parents=True, exist_ok=True)

        # Get the correct file extension from the generated audio file
        # VachanaTTS and Gemini generate .wav
        audio_extension = Path(source_path).suffix
        filename = f"question_{question_id}{audio_extension}"
        dest_path = audio_dir / filename

        shutil.copy2(source_path, dest_path)

        # Return absolute URL for frontend
        return f"{settings.server_url}/audio/{filename}"
