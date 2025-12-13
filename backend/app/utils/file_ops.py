"""
File operation utilities.
"""
import os
import logging
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


def cleanup_files(*file_paths: Union[str, Path]) -> None:
    """
    Clean up temporary files safely.

    Args:
        *file_paths: Variable number of file paths to delete

    Note:
        This function logs warnings but does not raise exceptions,
        as cleanup is best-effort operation.
    """
    for path in file_paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except OSError as e:
                logger.warning("Failed to cleanup %s: %s", path, e)
