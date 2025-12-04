from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
from typing import Optional
from dotenv import load_dotenv
from core.audio_processor import extract_audio, transcribe_audio
from core.ai_evaluator import evaluate_candidate
from core.tts_generator import generate_tts, TTSError
from pydantic import BaseModel
import asyncio

load_dotenv()

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequest(BaseModel):
    transcript: str
    question: str


class TTSRequest(BaseModel):
    text: str
    provider: str = "gemini"  # Default to Gemini TTS
    voice: Optional[str] = "kore"  # Use provider default if not specified


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    try:
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        # Extract audio and transcribe
        audio_path = extract_audio(file_location)
        transcript = transcribe_audio(audio_path)

        # Clean up temp files (optional, maybe keep for debugging for now)
        # os.remove(file_location)
        # os.remove(audio_path)

        return {"transcript": transcript, "filename": file_location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze")
async def analyze_interview(request: AnalysisRequest):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Google API Key not found")

    result = evaluate_candidate(api_key, request.question, request.transcript)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result


@app.post("/tts/generate")
async def generate_tts_audio(request: TTSRequest):
    """
    Generate audio from text using TTS.

    Use case: Generate audio for interview questions when displaying them to candidates.

    Args:
        request: TTSRequest containing text, provider (default: "gemini"), and optional voice

    Returns:
        dict: Contains audio_path to the generated audio file
    """
    try:
        # Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")

        # Generate TTS audio
        audio_path = await generate_tts(
            text=request.text,
            provider=request.provider,
            voice=request.voice,
            api_key=api_key
        )

        return {
            "success": True,
            "audio_path": audio_path,
            "provider": request.provider,
            "text_preview": request.text[:50] + "..." if len(request.text) > 50 else request.text
        }

    except TTSError as e:
        raise HTTPException(
            status_code=500, detail=f"TTS generation failed: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/tts/audio/{filename}")
async def get_tts_audio(filename: str):
    """
    Serve the generated TTS audio file.

    Args:
        filename: Name of the audio file (from the audio_path returned by /tts/generate)

    Returns:
        FileResponse: The audio file
    """
    # Security: Only allow files from temp directory
    # Extract just the filename without path for security

    filename = os.path.basename(filename)

    # Check if file exists in various possible locations
    possible_paths = [
        filename,  # Current directory
        os.path.join(os.getcwd(), filename),
        os.path.join(os.path.dirname(__file__), filename),
    ]

    for file_path in possible_paths:
        if os.path.exists(file_path):
            # Determine media type based on extension
            media_type = "audio/wav" if file_path.endswith(
                ".wav") else "audio/mpeg"
            return FileResponse(
                path=file_path,
                media_type=media_type,
                filename=filename
            )

    raise HTTPException(status_code=404, detail="Audio file not found")
