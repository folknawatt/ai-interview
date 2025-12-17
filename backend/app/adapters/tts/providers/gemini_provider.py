"""
Gemini TTS Provider implementation.

This module provides TTS generation using Google's Gemini AI service.
"""
import wave
import tempfile
from typing import Optional

from google import genai
from google.genai import types

from app.adapters.tts.tts_provider import TTSProvider
from app.adapters.tts.exceptions import (
    TTSProviderError,
    TTSConfigurationError,
)
from app.adapters.tts.constants import (
    GEMINI_MODEL,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_CHANNELS,
    DEFAULT_SAMPLE_WIDTH,
)
from app.config.logging_config import get_logger


logger = get_logger(__name__)


class GeminiTTSProvider(TTSProvider):
    """Gemini TTS provider implementation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        voice: str = "kore",
        sample_rate: int = DEFAULT_SAMPLE_RATE
    ):
        """
        Initialize Gemini TTS provider.

        Args:
            api_key: Google API key (if None, uses settings)
            voice: Voice name to use
            sample_rate: Audio sample rate

        Raises:
            TTSConfigurationError: If API key is not provided
        """
        if api_key is None:
            from app.config.settings import settings
            api_key = settings.google_api_key

        if not api_key:
            error_msg = (
                "Google API key not provided. "
                "Please set GOOGLE_API_KEY environment variable."
            )
            logger.error(error_msg)
            raise TTSConfigurationError(error_msg)

        self.api_key = api_key
        self.voice = voice
        self.sample_rate = sample_rate
        self.client = genai.Client(api_key=api_key)

    def get_provider_name(self) -> str:
        """Get provider name."""
        return "gemini"

    def generate_audio(
        self,
        text: str,
        output_path: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate audio using Gemini TTS.

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
            # Use tempfile to avoid cluttering root
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
                output_path = tf.name

        logger.info(
            "Generating Gemini TTS for text: '%s...' (voice: %s)",
            text[:50],
            voice
        )

        try:
            # Generate audio using Gemini TTS
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice,
                            )
                        )
                    ),
                )
            )

            # Extract audio data
            audio_data = response.candidates[0].content.parts[0].inline_data.data

            # Save as WAV file
            self._create_wave_file(output_path, audio_data)

            logger.info("Gemini TTS generation successful: %s", output_path)
            return output_path

        except (AttributeError, KeyError, IndexError) as e:
            error_msg = "Gemini TTS generation failed: %s"
            logger.error(error_msg, e)
            raise TTSProviderError(error_msg % str(e)) from e

    def _create_wave_file(
        self,
        filename: str,
        pcm_data: bytes
    ) -> None:
        """
        Create WAV file from PCM data.

        Args:
            filename: Output file path
            pcm_data: PCM audio data

        Raises:
            TTSProviderError: If file creation fails
        """
        try:
            with wave.open(filename, "wb") as wf:
                wf.setnchannels(DEFAULT_CHANNELS)
                wf.setsampwidth(DEFAULT_SAMPLE_WIDTH)
                wf.setframerate(self.sample_rate)
                wf.writeframes(pcm_data)
            logger.info("Wave file created successfully: %s", filename)
        except (IOError, OSError, RuntimeError) as e:
            logger.error("Failed to create wave file: %s", e)
            raise TTSProviderError(
                f"Failed to create wave file: {e}") from e
