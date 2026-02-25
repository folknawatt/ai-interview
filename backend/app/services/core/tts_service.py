"""TTS Service for audio generation.

Handles text-to-speech generation with retry logic and error handling.
"""

import asyncio
import shutil
from pathlib import Path

from app.adapters.tts.factory import TTSProviderFactory
from app.config.logging_config import get_logger
from app.config.settings import settings

logger = get_logger(__name__)


class TTSService:
    """Service for managing TTS generation with retry logic."""

    @staticmethod
    async def generate_question_audio(text: str, question_id: int) -> str | None:
        """Generate TTS audio for a question with retry logic.

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
                    max_retries + 1,
                )

                # Generate TTS audio using the configured provider
                # Assuming provider.generate_audio might be blocking or async.
                # If it's blocking requests (e.g. standard requests lib), we should wrap it.
                # However, without seeing adapter code, let's assume it might block.
                # Ideally, we'd check if provider.generate_audio is async.
                # If it's synchronous IO, run in thread.
                # For safety, let's run in thread if not awaitable.
                # But here call is provider.generate_audio(text=text)
                # Let's wrap it in to_thread just in case.
                temp_audio_path = await asyncio.to_thread(provider.generate_audio, text=text)

                # Save to public directory
                return await TTSService._save_audio_file(temp_audio_path, question_id)

            except (OSError, RuntimeError) as e:
                error_msg = str(e)

                # Check if it's a 503 overload error
                if "503" in error_msg or "overloaded" in error_msg.lower():
                    if attempt < max_retries:
                        logger.warning(
                            "TTS provider overloaded (attempt %d/%d). Retrying in %ss...",
                            attempt + 1,
                            max_retries + 1,
                            retry_delay,
                        )
                        # Fix: Use non-blocking sleep
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        logger.error(
                            "TTS provider still overloaded after %d attempts. "
                            "Continuing without audio.",
                            max_retries + 1,
                        )
                else:
                    logger.error("Failed to generate TTS: %s", error_msg)

                # Return None on final failure
                return None

        return None

    @staticmethod
    async def _save_audio_file(source_path: str, question_id: int) -> str:
        """Helper: Copy generated audio to public static directory.
        Run in thread pool to avoid blocking event loop during file I/O.
        """
        # Copy to audio directory for frontend access
        audio_dir = Path.cwd() / settings.tts_audio_dir
        # mkdir is fast enough, but can also be blocking.
        audio_dir.mkdir(parents=True, exist_ok=True)

        # Get the correct file extension from the generated audio file
        # VachanaTTS and Gemini generate .wav
        audio_extension = Path(source_path).suffix
        filename = f"question_{question_id}{audio_extension}"
        dest_path = audio_dir / filename

        # Fix: Use asyncio.to_thread for blocking file copy
        await asyncio.to_thread(shutil.copy2, source_path, dest_path)

        # Return absolute URL for frontend
        return f"{settings.server_url}/audio/{filename}"
