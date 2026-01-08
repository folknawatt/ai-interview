"""
Text-to-Speech API routes.

Provides endpoints for:
- Generating speech audio from text using various TTS providers
- Retrieving generated audio files
"""
import os
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from app.schemas import TTSRequest
from app.adapters.tts.factory import TTSProviderFactory
from app.adapters.tts.exceptions import TTSError, TTSConfigurationError
from app.exceptions import BadRequestError, NotFoundError, ServiceUnavailableError
from app.dependencies import get_api_key

router = APIRouter(
    prefix="/tts",
    tags=["Text to Speech"]
)


@router.post("/generate")
async def generate_tts_endpoint(
    request: TTSRequest,
    api_key: str = Depends(get_api_key)
) -> dict:
    """
    Generate text-to-speech audio from provided text.

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
        # Note: request.provider should be "gemini" or "edge"
        provider = TTSProviderFactory.create_provider(
            request.provider,
            api_key=api_key
        )

        # Generate audio (synchronous call)
        audio_path = provider.generate_audio(
            text=request.text
        )

        return {
            "success": True,
            "audio_path": audio_path,
            "filename": os.path.basename(audio_path)
        }
    except (TTSError, TTSConfigurationError) as e:
        raise ServiceUnavailableError(f"TTS generation failed: {e}") from e


@router.get("/audio/{filename}")
async def get_tts_file(filename: str) -> FileResponse:
    """
    Retrieve a generated TTS audio file.

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

    possible_path = os.path.abspath(filename)
    if os.path.exists(possible_path):
        return FileResponse(possible_path)

    raise NotFoundError("Audio file not found")
