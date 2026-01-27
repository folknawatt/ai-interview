"""
Edge TTS Provider implementation.

This module provides TTS generation using Microsoft Edge's online TTS service.
"""
import asyncio
import os
import time
from typing import Optional

import edge_tts

from app.adapters.tts.tts_provider import TTSProvider
from app.adapters.tts.exceptions import TTSProviderError
from app.adapters.tts.constants import AUDIO_OUTPUT_DIR
from app.config.logging_config import get_logger


logger = get_logger(__name__)

# Edge TTS timeout configuration (in seconds)
EDGE_TTS_CONNECT_TIMEOUT = 30
EDGE_TTS_RECEIVE_TIMEOUT = 60
EDGE_TTS_MAX_RETRIES = 3
EDGE_TTS_RETRY_DELAY = 2  # Initial delay in seconds


class EdgeTTSProvider(TTSProvider):
    """Edge TTS provider implementation."""

    def __init__(
        self,
        voice: str = "th-TH-PremwadeeNeural"
    ):
        """
        Initialize Edge TTS provider.

        Args:
            voice: Voice name to use (default: "th-TH-PremwadeeNeural")
            **kwargs: Additional arguments (ignored)
        """
        self.voice = voice

    def get_provider_name(self) -> str:
        """Get provider name."""
        return "edge"

    def generate_audio(
        self,
        text: str,
        output_path: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate audio using Edge TTS.

        This method wraps the async Edge TTS generation in a synchronous call
        to satisfy the TTSProvider interface.

        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            **kwargs: Additional parameters (voice override)

        Returns:
            str: Absolute path to generated audio file

        Raises:
            TTSProviderError: If generation fails
        """
        # Validate input
        self.validate_text(text)

        # Use voice from kwargs if provided, otherwise use default
        voice = kwargs.get("voice", self.voice)

        # Create output path if not provided
        if output_path is None:
            # Generate unique timestamp-based filename
            timestamp = int(time.time() * 1000)
            filename = f"edge_tts_{timestamp}.mp3"

            # Ensure audio directory exists
            audio_dir = os.path.join(os.getcwd(), AUDIO_OUTPUT_DIR)
            os.makedirs(audio_dir, exist_ok=True)
            output_path = os.path.join(audio_dir, filename)

        # Try to use existing event loop or create new one
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # If there's already a running loop, create a new one in a thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run,
                    self._generate_audio_with_retry(text, voice, output_path)
                )
                return future.result()
        else:
            return asyncio.run(
                self._generate_audio_with_retry(text, voice, output_path)
            )

    async def _generate_audio_with_retry(
        self,
        text: str,
        voice: str,
        output_path: str
    ) -> str:
        """
        Generate audio with retry logic for connection issues.

        Args:
            text: Text to convert
            voice: Voice to use
            output_path: Output path

        Returns:
            str: Output path
        """
        last_error = None
        retry_delay = EDGE_TTS_RETRY_DELAY

        for attempt in range(EDGE_TTS_MAX_RETRIES):
            try:
                logger.info(
                    "Generating Edge TTS (attempt %d/%d) for text: '%s...' (voice: %s)",
                    attempt + 1,
                    EDGE_TTS_MAX_RETRIES,
                    text[:50],
                    voice
                )

                # Generate with timeout
                result = await asyncio.wait_for(
                    self._generate_audio_async(text, voice, output_path),
                    timeout=EDGE_TTS_CONNECT_TIMEOUT + EDGE_TTS_RECEIVE_TIMEOUT
                )
                return result

            except asyncio.TimeoutError as e:
                last_error = e
                logger.warning(
                    "Edge TTS timeout (attempt %d/%d). Retrying in %ds...",
                    attempt + 1,
                    EDGE_TTS_MAX_RETRIES,
                    retry_delay
                )
                if attempt < EDGE_TTS_MAX_RETRIES - 1:
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff

            except Exception as e:
                # For connection errors, retry
                error_str = str(e).lower()
                if "timeout" in error_str or "connection" in error_str:
                    last_error = e
                    logger.warning(
                        "Edge TTS connection error (attempt %d/%d): %s. Retrying in %ds...",
                        attempt + 1,
                        EDGE_TTS_MAX_RETRIES,
                        str(e)[:100],
                        retry_delay
                    )
                    if attempt < EDGE_TTS_MAX_RETRIES - 1:
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2
                else:
                    # For other errors, fail immediately
                    raise TTSProviderError(
                        f"Edge TTS generation failed: {e}") from e

        # All retries exhausted
        error_msg = f"Edge TTS failed after {EDGE_TTS_MAX_RETRIES} attempts: {last_error}"
        logger.error(error_msg)
        raise TTSProviderError(error_msg)

    async def _generate_audio_async(
        self,
        text: str,
        voice: str,
        output_path: str
    ) -> str:
        """
        Internal async method to generate audio.

        Args:
            text: Text to convert
            voice: Voice to use
            output_path: Output path

        Returns:
            str: Output path
        """
        try:
            # Create communicator with proxy settings if needed
            communicate = edge_tts.Communicate(text, voice)

            # Save audio file
            await communicate.save(output_path)

            logger.info("Edge TTS generation successful: %s", output_path)
            return output_path

        except Exception as e:
            error_msg = f"Edge TTS generation failed: {e}"
            logger.error(error_msg)
            raise TTSProviderError(error_msg) from e
