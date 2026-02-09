"""
This module provides services for file storage operations.
"""
import os
from pathlib import Path
from typing import List, Union
import aiofiles
from fastapi import UploadFile

from app.config.logging_config import get_logger

logger = get_logger(__name__)


class StorageService:
    """
    Service for file storage operations.

    Provides abstraction layer for saving uploads and cleaning up temporary files.
    Uses async file I/O (aiofiles) for non-blocking file operations.
    """

    @staticmethod
    async def save_upload(file: UploadFile, directory: Path) -> Path:
        """
        Save uploaded file to disk asynchronously.

        Security: File validation should be done before calling this method.
        The caller is responsible for:
        - Validating file type/extension
        - Sanitizing filename
        - Checking file size limits

        Args:
            file: FastAPI UploadFile object (includes sanitized filename)
            directory: Target directory for saving file

        Returns:
            Absolute path to the saved file
        """
        # Ensure directory exists (create if needed)
        directory.mkdir(parents=True, exist_ok=True)
        file_path = directory / file.filename

        # Use async file I/O to avoid blocking event loop during write
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        return file_path

    @staticmethod
    def cleanup(files: List[Union[str, Path]]) -> None:
        """
        Remove temporary files from filesystem.

        This method is fail-safe - errors are logged but don't crash the application.
        Used for cleanup in finally blocks to prevent disk space accumulation.

        Args:
            files: List of file paths (str or Path) to remove
        """
        for file_path in files:
            try:
                if file_path:
                    path = Path(file_path)
                    if path.exists():
                        os.remove(path)
                        logger.debug("Cleaned up file: %s", file_path)
            except OSError as e:
                # Log but don't raise - cleanup should be fault-tolerant
                logger.error("Error cleaning up file %s: %s", file_path, e)
