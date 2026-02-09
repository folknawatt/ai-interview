"""
Media Service.

Handles media processing tasks such as audio extraction and transcription.
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from app.config.logging_config import get_logger

from app.adapters.ai.typhoon_asr import extract_audio, transcribe_audio
from app.services.core.storage_service import StorageService

logger = get_logger(__name__)


class MediaService:
    """
    Service for processing media files in the interview workflow.

    Handles the critical pipeline: Video -> Audio -> Transcript
    This is a CPU-intensive operation that uses thread pools to avoid blocking the async event loop.
    """

    @staticmethod
    async def process_video_to_transcript(video_path: str) -> Optional[str]:
        """
        Extract audio from video and transcribe to text using ASR.

        Processing pipeline:
        1. Extract audio from video file using FFmpeg (extract_audio)
        2. Transcribe audio to text using Typhoon ASR service (transcribe_audio)
        3. Clean up temporary audio file

        Both operations are CPU/network intensive and run in a thread pool
        to prevent blocking the async event loop.

        Args:
            video_path: Absolute path to uploaded video file

        Returns:
            Transcribed text from the video audio, or None if extraction fails

        Raises:
            Exception: Re-raises any errors from audio extraction or transcription
        """
        audio_path = None
        try:
            # Get current event loop for thread pool execution
            loop = asyncio.get_event_loop()

            # Run CPU-intensive operations in thread pool to avoid blocking
            with ThreadPoolExecutor() as pool:
                # Step 1: Extract audio from video (FFmpeg operation)
                audio_path = await loop.run_in_executor(
                    pool, extract_audio, video_path
                )

                # Step 2: Transcribe audio to text (ASR API call)
                transcript = await loop.run_in_executor(
                    pool, transcribe_audio, audio_path
                )
            return transcript

        except Exception as e:
            logger.error("Error processing media: %s", e)
            raise e

        finally:
            # Always cleanup temporary audio file to prevent disk space issues
            if audio_path:
                StorageService.cleanup([audio_path])
