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
    """Service for abstracting file storage operations."""

    @staticmethod
    async def save_upload(file: UploadFile, directory: Path) -> Path:
        """
        Save an uploaded file to the specified directory.

        Args:
            file: The uploaded file object.
            directory: The target directory path.

        Returns:
            Path: The absolute path to the saved file.
        """
        directory.mkdir(parents=True, exist_ok=True)
        file_path = directory / file.filename

        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        return file_path

    @staticmethod
    def cleanup(files: List[Union[str, Path]]) -> None:
        """
        Remove specified files from the filesystem.

        Args:
            files: List of file paths to remove.
        """
        for file_path in files:
            try:
                if file_path:
                    path = Path(file_path)
                    if path.exists():
                        os.remove(path)
            except OSError as e:
                logger.error("Error cleaning up file %s: %s", file_path, e)
