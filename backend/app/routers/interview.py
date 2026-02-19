"""
Candidate Interview API routes.

Provides endpoints for candidates to:
- Retrieve interview questions for selected role
- Upload video answers for evaluation
- Get interview session summary and results
"""
import json
from typing import Any
from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.dependencies import get_api_key
from app.services import InterviewService, QuestionService
from app.services.core.tts_service import TTSService
from app.services.core.role_service import RoleService
from app.services.interview.resume_service import ResumeService
from app.exceptions import NotFoundError
from app.schemas.interview import UploadPDFResponse, QuestionResponse
from app.config.logging_config import get_logger


logger = get_logger(__name__)

router = APIRouter(
    prefix="/interview",
    tags=["Candidate Interview"]
)


@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile,
    role_id: str = Form(..., description="Role ID to add questions to"),
    candidate_name: str = Form(..., description="Candidate Name"),
    candidate_email: str = Form(None, description="Candidate Email"),
    db: AsyncSession = Depends(get_db)
) -> UploadPDFResponse:
    """
    Upload PDF resume, generate custom questions, and initialize interview session.

    This endpoint implements the "Snapshot Pattern":
    1. Extract text from PDF resume
    2. Generate AI-powered custom questions based on resume
    3. Combine base role questions + custom resume questions
    4. Create interview session with snapshot of all questions

    The snapshot ensures questions don't change even if the role's base questions are updated later.
    """
    # Read uploaded PDF file into memory
    pdf_bytes = await file.read()

    # Generate AI questions from PDF resume
    service = ResumeService()
    result_json_str = service.generate_questions_from_pdf(
        pdf_bytes=pdf_bytes, num_questions=2  # Generate 2 custom questions from resume
    )

    try:
        questions_list = json.loads(result_json_str)
    except json.JSONDecodeError as exc:
        raise ValueError('AI Service returned invalid JSON format') from exc

    if not isinstance(questions_list, list):
        raise ValueError("AI Service did not return a list of questions")

    # Fetch base role questions
    role_data = await RoleService.get_role_by_id(db, role_id)
    base_questions = [q['content'] for q in role_data.get('questions', [])]

    # Combine: base questions first, then custom
    all_questions = base_questions + questions_list

    # Create session with question snapshot
    session_id = await InterviewService.init_session_with_questions(
        db, role_id, all_questions, candidate_name, candidate_email
    )

    return UploadPDFResponse(
        session_id=session_id,
        role_id=role_id,
        questions=all_questions
    )


@router.get("/question/{role_id}/{index}")
async def get_interview_question(
    role_id: str,
    index: int,
    db: AsyncSession = Depends(get_db)
) -> QuestionResponse:
    """Get interview question by role and index (Legacy/Standard Flow)."""
    # Note: QuestionService.get_next_question involves RoleService (file-based), so it remains sync
    result = await QuestionService.get_next_question(db, role_id, index)
    if not result:
        raise NotFoundError(f"Role '{role_id}' not found")

    # Generate TTS audio for the question if status is "continue"
    if result.get("status") == "continue" and "question" in result:
        result["audio_path"] = await TTSService.generate_question_audio(
            text=result["question"],
            question_id=result["question_id"]
        )

    return result


@router.get("/session/{session_id}/question/{index}")
async def get_session_question(
    session_id: str,
    index: int,
    skip_tts: bool = False,
    db: AsyncSession = Depends(get_db)
) -> QuestionResponse:
    """
    Get interview question from session snapshot.

    Uses the question snapshot saved during session initialization.
    This ensures questions remain consistent throughout the interview.

    Args:
        session_id: Interview session ID
        index: Question index (0-based, starts at 0)
        skip_tts: If True, skip TTS generation (useful for pre-checking next question)

    Returns:
        QuestionResponse with question text, question_id, status, and optional audio_path
    """
    result = await QuestionService.get_session_question(db, session_id, index)

    if not result:
        # If no questions found in session, likely invalid session
        raise NotFoundError(f"Session '{session_id}' not found")

    # Generate TTS audio if needed
    if result.get("status") == "continue" and "question" in result and not skip_tts:
        result["audio_path"] = await TTSService.generate_question_audio(
            text=result["question"],
            question_id=result["question_id"]
        )
    else:
        result["audio_path"] = None

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
    session: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
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
async def complete_interview(
    session_id: str,
    session: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    """Mark interview as complete and calculate aggregated scores."""
    return await InterviewService.complete_interview(session, session_id)


@router.get("/summary/{session_id}")
async def get_summary(
    session_id: str,
    session: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    """Get interview summary from database."""
    return await InterviewService.get_summary(session, session_id)
