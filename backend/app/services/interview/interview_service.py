"""Interview Service.

Encapsulates business logic for candidate interviews:
- Answer processing (Video -> Transcript -> AI Evaluation)
- Session and candidate management
- Scoring and summaries
"""

import asyncio
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logging_config import get_logger
from app.config.settings import settings
from app.database.models import (
    InterviewSession,
    InterviewStatus,
    QuestionResult,
)
from app.exceptions import (
    BadGatewayError,
    NotFoundError,
    ServiceUnavailableError,
    ValidationError,
)
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.interview_repository import InterviewRepository
from app.services.core.mappers import InterviewMapper
from app.services.core.media_service import MediaService
from app.services.core.role_service import RoleService
from app.services.core.storage_service import StorageService
from app.services.scoring.aggregator import calculate_aggregated_score
from app.services.scoring.evaluator import evaluate_candidate

logger = get_logger(__name__)

VIDEO_DIR = Path(settings.base_storage_dir) / "videos"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)


class InterviewService:
    """Service class for handling interview business logic."""

    @staticmethod
    async def process_answer(
        session: AsyncSession,
        api_key: str,
        file: UploadFile,
        question_id: int,
        question: str,
        candidate_data: dict[str, str],
        candidate_repo: CandidateRepository,
        interview_repo: InterviewRepository,
    ) -> dict[str, Any]:
        """Complete pipeline for processing a candidate's video answer:
        1. Save uploaded video
        2. Extract transcript from video
        3. Evaluate answer with AI
        4. Persist results and generate next dynamic question
        """
        session_id = candidate_data["session_id"]
        role_id = candidate_data["role_id"]
        name = candidate_data["name"]
        email = candidate_data.get("email")

        candidate = await candidate_repo.get_or_create(name, email)

        # Ensure interview session exists
        interview_session = await interview_repo.get_by_session_id(session_id)
        if not interview_session:
            interview_session = InterviewSession(
                session_id=session_id,
                candidate_id=candidate.id,
                role_id=role_id,
                status=InterviewStatus.IN_PROGRESS,
            )
            await interview_repo.create(interview_session)

        file_location: Path | None = None
        cleanup_needed = True
        video_url: str | None = None

        try:
            # Save video with a unique filename
            file_ext = Path(file.filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file.filename = unique_filename
            file_location = await StorageService.save_upload(file, VIDEO_DIR)
            video_url = f"/videos/{unique_filename}"

            # Transcribe video
            role_title = await RoleService.get_role_title(session, role_id)
            transcript = await MediaService.process_video_to_transcript(str(file_location))

            # Evaluate answer with AI (CPU-bound → run in thread)
            evaluation = await asyncio.to_thread(
                evaluate_candidate, api_key, question, transcript, role_title
            )

            # Persist question result
            question_result = await InterviewService._save_question_result(
                interview_repo,
                session_id,
                question_id,
                question,
                transcript,
                evaluation,
                video_url,
            )

            cleanup_needed = False
            return InterviewMapper.to_dict(question_result)

        except ValueError as e:
            logger.warning("Validation error: %s", e)
            raise ValidationError(str(e)) from e

        except ConnectionError as e:
            logger.error("Connection error: %s", e)
            raise ServiceUnavailableError("AI Service unavailable") from e

        except RuntimeError as e:
            logger.error("Runtime error: %s", e)
            raise BadGatewayError("AI Service error") from e

        except Exception:
            logger.error("Unexpected error processing answer", exc_info=True)
            raise

        finally:
            if cleanup_needed and file_location:
                StorageService.cleanup([file_location])

    @staticmethod
    async def complete_interview(
        session: AsyncSession, session_id: str, interview_repo: InterviewRepository
    ) -> dict[str, Any]:
        """Finalize the interview and calculate aggregated scores."""
        logger.info("Completing interview for session: %s", session_id)

        interview_session = await interview_repo.get_by_session_id(session_id)
        if not interview_session:
            raise NotFoundError("Interview session not found")

        question_results = await interview_repo.get_question_results(session_id)
        if not question_results:
            logger.warning("No question results found for session: %s", session_id)
            raise ValidationError("No question results found for this session")

        total_questions = len(question_results)
        aggregated_score_result = calculate_aggregated_score(question_results, total_questions)

        # Save or update aggregated score
        existing_score = await interview_repo.get_aggregated_score(session_id)
        if existing_score:
            existing_score.average_score = aggregated_score_result.average_score
            existing_score.communication_avg = aggregated_score_result.communication_avg
            existing_score.relevance_avg = aggregated_score_result.relevance_avg
            existing_score.logical_thinking_avg = aggregated_score_result.logical_thinking_avg
            existing_score.pass_rate = aggregated_score_result.pass_rate
            existing_score.overall_recommendation = aggregated_score_result.overall_recommendation
            existing_score.questions_answered = aggregated_score_result.questions_answered
            existing_score.total_questions = aggregated_score_result.total_questions
            await interview_repo.update(existing_score)
        else:
            aggregated_score_result.session_id = session_id
            await interview_repo.create(aggregated_score_result)

        # Mark session as completed
        interview_session.status = InterviewStatus.COMPLETED
        interview_session.completed_at = datetime.now(UTC)
        await interview_repo.update(interview_session)

        return {
            "message": "Interview completed successfully",
            "session_id": session_id,
            "recommendation": aggregated_score_result.overall_recommendation,
            "average_score": aggregated_score_result.average_score,
        }

    @staticmethod
    async def init_session_with_questions(
        role_id: str,
        questions: list[str],
        candidate_repo: CandidateRepository,
        interview_repo: InterviewRepository,
        candidate_name: str = "Anonymous",
        candidate_email: str | None = None,
    ) -> str:
        """Initialize a new interview session with a snapshot of questions.

        The snapshot pattern ensures questions remain stable even if the role's
        base questions are updated after the session starts.
        """
        candidate = await candidate_repo.get_or_create(candidate_name, candidate_email)
        session_id = f"sess_{uuid.uuid4().hex[:12]}"

        interview_session = InterviewSession(
            session_id=session_id,
            candidate_id=candidate.id,
            role_id=role_id,
            status=InterviewStatus.STARTED,
        )
        await interview_repo.create(interview_session)

        for q_text in questions:
            qr = QuestionResult(
                session_id=session_id,
                question=q_text,
                communication_score=0.0,
                relevance_score=0.0,
                logical_thinking_score=0.0,
                pass_prediction=False,
                feedback={},
            )
            await interview_repo.save_question_result(qr)

        return session_id

    @staticmethod
    async def get_summary(
        session: AsyncSession, session_id: str, interview_repo: InterviewRepository
    ) -> dict[str, Any]:
        """Retrieve interview summary with question results and aggregated scores."""
        interview_session = await interview_repo.get_by_session_id(session_id)
        if not interview_session:
            raise NotFoundError("Session not found")

        question_results = await interview_repo.get_question_results(session_id)
        results = [InterviewMapper.to_dict(qr) for qr in question_results]

        aggregated_score = await interview_repo.get_aggregated_score(session_id)
        aggregated_data = None
        if aggregated_score:
            aggregated_data = {
                "average_score": aggregated_score.average_score,
                "communication_avg": aggregated_score.communication_avg,
                "relevance_avg": aggregated_score.relevance_avg,
                "logical_thinking_avg": aggregated_score.logical_thinking_avg,
                "pass_rate": aggregated_score.pass_rate,
                "overall_recommendation": aggregated_score.overall_recommendation,
                "questions_answered": aggregated_score.questions_answered,
                "total_questions": aggregated_score.total_questions,
            }

        return {
            "total_questions": len(results),
            "details": results,
            "aggregated_score": aggregated_data,
        }

    @staticmethod
    async def _save_question_result(
        interview_repo: InterviewRepository,
        session_id: str,
        question_id: int,
        question: str,
        transcript: str | None,
        evaluation: Any,
        video_url: str | None,
    ) -> QuestionResult:
        """Save or update a question result snapshot in the database."""
        existing_qr = await interview_repo.get_question_result(session_id, question)

        if existing_qr:
            existing_qr.transcript = transcript
            existing_qr.communication_score = evaluation.scores.communication
            existing_qr.relevance_score = evaluation.scores.relevance
            existing_qr.logical_thinking_score = evaluation.scores.logical_thinking
            existing_qr.pass_prediction = evaluation.pass_prediction
            existing_qr.feedback = {
                "strengths": evaluation.feedback.strengths,
                "weaknesses": evaluation.feedback.weaknesses,
                "summary": evaluation.feedback.summary,
            }
            if video_url:
                existing_qr.video_url = video_url
            return await interview_repo.update(existing_qr)

        # Fallback: create new record (should not occur in normal snapshot flow)
        question_result = InterviewMapper.to_orm_question_result(
            session_id, question_id, question, transcript, evaluation
        )
        if video_url:
            question_result.video_url = video_url
        return await interview_repo.save_question_result(question_result)
