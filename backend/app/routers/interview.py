"""
Candidate Interview API routes.

Provides endpoints for candidates to:
- Retrieve interview questions for selected role
- Upload video answers for evaluation
- Get interview session summary and results
"""
from typing import Dict, Any

from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.dependencies import get_api_key
from app.services import InterviewService, QuestionService
from app.services.core.tts_service import TTSService
from app.exceptions import NotFoundError
from app.config.logging_config import get_logger


logger = get_logger(__name__)

router = APIRouter(
    prefix="/interview",
    tags=["Candidate Interview"]
)


@router.get("/question/{role_id}/{index}")
async def get_interview_question(role_id: str, index: int) -> Dict[str, Any]:
    """Get interview question by role and index with TTS audio."""
    result = QuestionService.get_next_question(role_id, index)
    if not result:
        raise NotFoundError(f"Role '{role_id}' not found")

    # Generate TTS audio for the question if status is "continue"
    if result.get("status") == "continue" and "question" in result:
        result["audio_path"] = TTSService.generate_question_audio(
            text=result["question"],
            question_id=result["question_id"]
        )

    return result


@router.post("/upload-answer")
async def upload_and_analyze(
    file: UploadFile = File(...),
    question: str = Form(...),
    question_id: int = Form(...),
    session_id: str = Form(...),
    role_id: str = Form(...),
    candidate_name: str = Form(...),
    candidate_email: str = Form(None),
    api_key: str = Depends(get_api_key),
    session: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Upload video answer and analyze with AI evaluation."""
    candidate_data = {
        "session_id": session_id,
        "role_id": role_id,
        "name": candidate_name,
        "email": candidate_email
    }
    # Exceptions are handled by global exception handler in main.py
    return await InterviewService.process_answer(
        session, api_key, file, question_id, question, candidate_data
    )


@router.post("/complete/{session_id}")
def complete_interview(
    session_id: str,
    session: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Mark interview as complete and calculate aggregated scores."""
    return InterviewService.complete_interview(session, session_id)


@router.get("/summary/{session_id}")
def get_summary(
    session_id: str,
    session: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get interview summary from database."""
    return InterviewService.get_summary(session, session_id)
