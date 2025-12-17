"""
TTS Service for audio generation.

Handles text-to-speech generation with retry logic and error handling.
"""
import os
import shutil
import time
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
                audio_path = provider.generate_audio(text=text)

                # Copy to audio directory for frontend access
                audio_dir = os.path.join(os.getcwd(), settings.tts_audio_dir)
                os.makedirs(audio_dir, exist_ok=True)

                filename = f"question_{question_id}.wav"
                dest_path = os.path.join(audio_dir, filename)
                shutil.copy2(audio_path, dest_path)

                # Return absolute URL for frontend
                return f"{settings.server_url}/audio/{filename}"

            except (OSError, RuntimeError) as e:
                error_msg = str(e)

                # Check if it's a 503 overload error
                if "503" in error_msg or "overloaded" in error_msg.lower():
                    if attempt < max_retries:
                        logger.warning(
                            "Gemini TTS overloaded (attempt %d/%d). Retrying in %ss...",
                            attempt + 1, max_retries + 1, retry_delay
                        )
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        logger.error(
                            "Gemini TTS still overloaded after %d attempts. "
                            "Continuing without audio.",
                            max_retries + 1
                        )
                else:
                    logger.error("Failed to generate TTS: %s", error_msg)

                # Return None on final failure
                return None

        return None
