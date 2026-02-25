"""Text-to-Speech API routes.

Provides endpoints for:
- Generating speech audio from text using various TTS providers
- Retrieving generated audio files
"""

import os
from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.adapters.tts.exceptions import TTSConfigurationError, TTSError
from app.adapters.tts.factory import TTSProviderFactory
from app.config.settings import settings
from app.dependencies import get_api_key
from app.exceptions import BadRequestError, NotFoundError, ServiceUnavailableError
from app.schemas import TTSRequest

router = APIRouter(prefix="/tts", tags=["Text to Speech"])


@router.post("/generate")
async def generate_tts_endpoint(request: TTSRequest, api_key: str = Depends(get_api_key)) -> dict:
    """Generate text-to-speech audio from provided text.

    Args:
        request: TTS request containing text and provider information
        api_key: Google API key (injected via dependency)

    Returns:
        dict: Response containing success status, audio file path, and filename

    Raises:
        HTTPException: If TTS generation fails
    """
    try:
        # Create provider using factory
        # Note: request.provider should be "gemini" or "vachana"
        provider = TTSProviderFactory.create_provider(request.provider, api_key=api_key)

        # Generate audio (synchronous call)
        audio_path = provider.generate_audio(text=request.text)

        return {"success": True, "audio_path": audio_path, "filename": os.path.basename(audio_path)}
    except (TTSError, TTSConfigurationError) as e:
        raise ServiceUnavailableError(f"TTS generation failed: {e}") from e


@router.get("/audio/{filename}")
async def get_tts_file(filename: str) -> FileResponse:
    """Retrieve a generated TTS audio file.

    Args:
        filename: Name of the audio file to retrieve

    Returns:
        FileResponse: The requested audio file

    Raises:
        HTTPException: If filename is invalid or file not found
    """
    # Basic path security validation (check both Unix and Windows path separators)
    if ".." in filename or "/" in filename or "\\" in filename:
        raise BadRequestError("Invalid filename")

    # Resolve the audio directory and the requested file path
    audio_dir = Path(settings.tts_audio_dir).resolve()
    file_path = (audio_dir / filename).resolve()

    # Ensure the resolved path is strictly within the audio directory (prevent path traversal)
    if not str(file_path).startswith(str(audio_dir)):
        raise BadRequestError("Invalid filename")

    if file_path.exists():
        return FileResponse(file_path)

    raise NotFoundError("Audio file not found")
