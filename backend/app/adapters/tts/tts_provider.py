"""Abstract base class for TTS providers.

This module defines the interface that all TTS providers must implement,
enabling flexible switching between different TTS services.
"""

from abc import ABC, abstractmethod


class TTSProvider(ABC):
    """Abstract base class for Text-to-Speech providers.

    All TTS provider implementations must inherit from this class
    and implement the required abstract methods.
    """

    @abstractmethod
    def generate_audio(self, text: str, output_path: str | None = None, **kwargs) -> str:
        """Generate audio from text.

        Args:
            text: Text to convert to speech
            output_path: Optional path to save audio file
            **kwargs: Additional provider-specific parameters

        Returns:
            str: Path or URL to the generated audio file

        Raises:
            TTSError: If audio generation fails
        """
        raise NotImplementedError

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of the TTS provider.

        Returns:
            str: Provider name (e.g., "gemini", "edge")
        """
        raise NotImplementedError

    def validate_text(self, text: str) -> None:
        """Validate input text before processing.

        Args:
            text: Text to validate

        Raises:
            ValueError: If text is empty or invalid
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        if len(text) > 5000:  # Reasonable limit for TTS
            raise ValueError("Text exceeds maximum length of 5000 characters")
