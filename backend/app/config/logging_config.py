"""
Centralized logging configuration for AI Interview system.

This module provides a standardized logging setup for all modules.
"""
import logging
import sys
from pythonjsonlogger import jsonlogger


def configure_logging(log_level: str = "INFO", json_format: bool = True):
    """
    Configure global logging for the application.

    JSON format provides structured logs that are easier to parse in production
    environments for log aggregation services (e.g., CloudWatch, Datadog).

    Args:
        log_level: Logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
        json_format: If True, outputs structured JSON logs; if False, plain text
    """
    logger = logging.getLogger()

    # Remove existing handlers to avoid duplication during hot-reloads in development
    # This is critical for uvicorn --reload mode
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.setLevel(log_level)

    stream_handler = logging.StreamHandler(sys.stdout)

    if json_format:
        # JSON formatter for production: structured logs with timestamp, level, module, message
        # Fields are renamed for clarity: 'asctime' -> 'timestamp', 'levelname' -> 'level'
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            rename_fields={"asctime": "timestamp", "levelname": "level"}
        )
    else:
        # Standard formatter for development: human-readable plain text
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Reduce noise from verbose libraries
    # uvicorn.access logs every HTTP request - we only care about errors
    # aiosqlite can be very chatty with query logging
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name (str): Name of the module (typically __name__)

    Returns:
        logging.Logger: Logger instance for the module
    """
    return logging.getLogger(name)
