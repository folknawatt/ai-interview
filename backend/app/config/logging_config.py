"""
Centralized logging configuration for AI Interview system.

This module provides a standardized logging setup for all modules.
"""
import logging


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name (str): Name of the module (typically __name__)

    Returns:
        logging.Logger: Logger instance for the module
    """
    return logging.getLogger(name)
