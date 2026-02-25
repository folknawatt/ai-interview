"""Centralized exception handling for AI Interview system.

This module provides:
- Custom exception classes with built-in HTTP status codes
- Automatic exception-to-HTTP-status mapping
- Clean separation of business logic from error handling
"""

from app.config.logging_config import get_logger

logger = get_logger(__name__)


class AppException(Exception):
    """Base application exception with HTTP status code.

    All custom exceptions should inherit from this class.
    The global exception handler in main.py will automatically
    convert these to appropriate HTTP responses.
    """

    status_code: int = 500
    default_detail: str = "Internal server error"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class NotFoundError(AppException):
    """Resource not found (404)."""

    status_code = 404
    default_detail = "Resource not found"


class ValidationError(AppException):
    """Validation or processing error (422)."""

    status_code = 422
    default_detail = "Validation error"


class BadRequestError(AppException):
    """Bad request error (400)."""

    status_code = 400
    default_detail = "Bad request"


class ForbiddenError(AppException):
    """Permission denied (403)."""

    status_code = 403
    default_detail = "Permission denied"


class ServiceUnavailableError(AppException):
    """External service unavailable (503)."""

    status_code = 503
    default_detail = "Service temporarily unavailable"


class BadGatewayError(AppException):
    """External service error (502)."""

    status_code = 502
    default_detail = "External service error"


class ConfigurationError(AppException):
    """Configuration or setup error (500)."""

    status_code = 500
    default_detail = "Configuration error"


class AudioProcessingError(AppException):
    """Audio/video processing error (500)."""

    status_code = 500
    default_detail = "Audio processing failed"


class TranscriptionError(AppException):
    """Transcription error (500)."""

    status_code = 500
    default_detail = "Transcription failed"


class DatabaseError(AppException):
    """Database operation error (500)."""

    status_code = 500
    default_detail = "Database operation failed"


# Exception mapping for automatic conversion
EXCEPTION_MAP = {
    ValueError: (422, "Invalid value"),
    ConnectionError: (503, "Service temporarily unavailable"),
    RuntimeError: (502, "External service error"),
    FileNotFoundError: (404, "File not found"),
    PermissionError: (403, "Permission denied"),
    KeyError: (404, "Resource not found"),
    IOError: (500, "I/O operation failed"),
    OSError: (500, "System operation failed"),
    TimeoutError: (503, "Request timeout"),
}


def convert_exception(exc: Exception) -> AppException:
    """Convert standard Python exceptions to AppException.

    Args:
        exc: The original exception

    Returns:
        AppException with appropriate status code
    """
    exc_type = type(exc)

    if exc_type in EXCEPTION_MAP:
        status_code, default_msg = EXCEPTION_MAP[exc_type]
        detail = str(exc) if str(exc) else default_msg

        # Create appropriate AppException subclass
        if status_code == 422:
            return ValidationError(detail)
        elif status_code == 503:
            return ServiceUnavailableError(detail)
        elif status_code == 502:
            return BadGatewayError(detail)
        elif status_code == 404:
            return NotFoundError(detail)
        elif status_code == 403:
            return ForbiddenError(detail)

    # Default to internal server error
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return AppException(f"Internal error: {str(exc)}")
