"""
VachanaTTS Provider implementation.

This module provides TTS generation using vachanatts library.
"""
import os
import time
from typing import Optional

from vachanatts import TTS

from app.adapters.tts.tts_provider import TTSProvider
from app.adapters.tts.exceptions import TTSProviderError
from app.adapters.tts.constants import AUDIO_OUTPUT_DIR
from app.config.logging_config import get_logger


logger = get_logger(__name__)


class VachanaTTSProvider(TTSProvider):
    """VachanaTTS provider implementation."""

    def __init__(
        self,
        voice: str = "th_f_1",
        speed: float = 1.0,
        volume: float = 1.0
    ):
        """
        Initialize VachanaTTS provider.

        Args:
            voice: Voice name to use (default: "th_f_1")
            speed: Speech speed (default: 1.0)
            volume: Speech volume (default: 1.0)
        """
        self.voice = voice
        self.speed = speed
        self.volume = volume

    def get_provider_name(self) -> str:
        """Get provider name."""
        return "vachana"

    def generate_audio(
        self,
        text: str,
        output_path: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate audio using VachanaTTS.

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
            filename = f"vachana_tts_{timestamp}.wav"

            # Ensure audio directory exists
            audio_dir = os.path.join(os.getcwd(), AUDIO_OUTPUT_DIR)
            os.makedirs(audio_dir, exist_ok=True)
            output_path = os.path.join(audio_dir, filename)

        try:
            logger.info(
                "Generating VachanaTTS for text: '%s...' (voice: %s)", text[:50], voice)

            # vachanatts.TTS seems to be a function that runs immediately
            TTS(
                text,
                voice=voice,
                output=output_path,
                volume=self.volume,
                speed=self.speed
            )

            if not os.path.exists(output_path):
                raise TTSProviderError(
                    "Output file was not created by VachanaTTS")

            logger.info("VachanaTTS generation successful: %s", output_path)
            return output_path

        except Exception as e:
            error_msg = f"VachanaTTS generation failed: {e}"
            logger.error(error_msg)
            raise TTSProviderError(error_msg) from e
