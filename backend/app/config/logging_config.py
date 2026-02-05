"""
Centralized logging configuration for AI Interview system.

This module provides a standardized logging setup for all modules.
"""
import logging
import sys
from pythonjsonlogger import jsonlogger


def configure_logging(log_level: str = "INFO", json_format: bool = True):
    """
    Configure global logging.

    Args:
        log_level: Logging level (INFO, DEBUG, etc.)
        json_format: Whether to output logs in JSON format
    """
    logger = logging.getLogger()

    # Remove existing handlers to avoid duplication during reloads
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.setLevel(log_level)

    stream_handler = logging.StreamHandler(sys.stdout)

    if json_format:
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            rename_fields={"asctime": "timestamp", "levelname": "level"}
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Silence noisy libraries
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
