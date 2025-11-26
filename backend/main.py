from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from dotenv import load_dotenv
from core.audio_processor import extract_audio, transcribe_audio
from core.ai_evaluator import evaluate_candidate
from pydantic import BaseModel

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
