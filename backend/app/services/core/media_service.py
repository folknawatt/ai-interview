"""
Media Service.

Handles media processing tasks such as audio extraction and transcription.
"""
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from app.adapters.ai.typhoon_asr import extract_audio, transcribe_audio
from app.services.core.storage_service import StorageService

logger = logging.getLogger(__name__)


class MediaService:
    """Service for handling media files (Audio/Video)."""

    @staticmethod
    async def process_video_to_transcript(video_path: str) -> Optional[str]:
        """
        Extract audio from video and transcribe it.

        Args:
            video_path (str): Path to the video file.

        Returns:
            Optional[str]: Transcribed text or None if failed.
        """
        audio_path = None
        try:
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as pool:
                audio_path = await loop.run_in_executor(
                    pool, extract_audio, video_path
                )
                transcript = await loop.run_in_executor(
                    pool, transcribe_audio, audio_path
                )
            return transcript
        except Exception as e:
            logger.error("Error processing media: %s", e)
            raise e
        finally:
            if audio_path:
                StorageService.cleanup([audio_path])
