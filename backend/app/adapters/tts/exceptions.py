"""TTS Exceptions."""

from app.exceptions import AppException


class TTSError(AppException):
    """Base exception for TTS-related errors."""

    status_code = 500
    default_detail = "TTS generation failed"


class TTSProviderError(TTSError):
    """Exception raised when TTS provider fails."""

    status_code = 502
    default_detail = "TTS provider error"


class TTSConfigurationError(TTSError):
    """Exception raised for TTS configuration errors."""

    status_code = 500
    default_detail = "TTS configuration error"
