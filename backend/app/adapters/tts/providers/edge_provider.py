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

        return asyncio.run(self._generate_audio_async(text, voice, output_path))

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
        logger.info(
            "Generating Edge TTS for text: '%s...' (voice: %s)",
            text[:50],
            voice
        )

        try:
            # Create communicator
            communicate = edge_tts.Communicate(text, voice)

            # Save audio file
            await communicate.save(output_path)

            logger.info("Edge TTS generation successful: %s", output_path)
            return output_path

        except Exception as e:
            error_msg = f"Edge TTS generation failed: {e}"
            logger.error(error_msg)
            raise TTSProviderError(error_msg) from e
