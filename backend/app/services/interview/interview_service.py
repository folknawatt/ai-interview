"""
Interview Service.

Encapsulates business logic for candidate interviews, including:
- Candidate management
- Answer processing (Video -> Audio -> Transcript -> AI Evaluation)
- Scoring and Summaries
"""
import asyncio
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import UploadFile
from sqlmodel import Session, select

from app.config.settings import settings
from app.database.models import (
    AggregatedScore,
    InterviewSession,
    InterviewStatus,
    QuestionResult,
)
from app.services.scoring.aggregator import calculate_aggregated_score
from app.services.scoring.evaluator import evaluate_candidate
from app.exceptions import (
    NotFoundError,
    ValidationError,
    ServiceUnavailableError,
    BadGatewayError,
)
from app.services.interview.candidate_service import CandidateService
from app.services.core.mappers import InterviewMapper
from app.services.core.media_service import MediaService
from app.services.interview.question_service import QuestionService
from app.services.core.storage_service import StorageService

logger = logging.getLogger(__name__)

TEMP_DIR = Path(settings.temp_storage_dir)


class InterviewService:
    """Service class for handling interview business logic."""

    @staticmethod
    async def process_answer(
        session: Session,
        api_key: str,
        file: UploadFile,
        question_id: int,
        question: str,
        candidate_data: Dict[str, str],
    ) -> Dict[str, Any]:
        """
        Upload video, extract audio, transcribe, and evaluate.

        Args:
            session: Database session.
            api_key: API key for evaluation service.
            file: Uploaded video file.
            question: The interview question text.
            candidate_data: Dictionary containing candidate and session info.

        Returns:
            Dict containing the question result details.
        """
        session_id = candidate_data["session_id"]
        role_id = candidate_data["role_id"]
        name = candidate_data["name"]
        email = candidate_data.get("email")

        # Get or create candidate
        candidate = CandidateService.get_or_create(session, name, email)

        # Get or create interview session
        InterviewService._get_or_create_session(
            session, session_id, candidate.id, role_id
        )

        file_location: Optional[Path] = None

        try:
            # Save video file
            file_ext = Path(file.filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file.filename = unique_filename

            file_location = await StorageService.save_upload(file, TEMP_DIR)

            # Fetch role title
            role_title = QuestionService.get_role_title(role_id)

            # Process media (Video -> Audio -> Transcript)
            transcript = await MediaService.process_video_to_transcript(
                str(file_location)
            )

            # Evaluate Candidate Answer
            # Run CPU-bound/network-bound synchronous evaluation in a thread
            loop = asyncio.get_event_loop()
            evaluation = await loop.run_in_executor(
                None, evaluate_candidate, api_key, question, transcript, role_title
            )

            # Cleanup Video File (Audio is handled by MediaService)
            if file_location:
                StorageService.cleanup([file_location])

            # Save result using Mapper
            question_result = InterviewMapper.to_orm_question_result(
                session_id, question_id, question, transcript, evaluation
            )
            session.add(question_result)
            session.commit()
            session.refresh(question_result)

            return InterviewMapper.to_dict(question_result)

        except ValueError as e:
            # Input error (empty transcript or bad format)
            if file_location:
                StorageService.cleanup([file_location])
            logger.warning("Validation error in process_answer: %s", e)
            raise ValidationError(str(e)) from e

        except ConnectionError as e:
            # External service unavailable
            if file_location:
                StorageService.cleanup([file_location])
            logger.error("Connection error in process_answer: %s", e)
            raise ServiceUnavailableError(
                "AI Service temporarily unavailable") from e

        except RuntimeError as e:
            # External service error
            if file_location:
                StorageService.cleanup([file_location])
            logger.error("Runtime error in process_answer: %s", e)
            raise BadGatewayError("AI Service returned an error") from e

        except Exception as e:
            # Cleanup files before re-raising
            if file_location:
                StorageService.cleanup([file_location])
            logger.error("Error processing answer: %s", e)
            raise

    @classmethod
    def complete_interview(cls, session: Session, session_id: str) -> Dict[str, Any]:
        """
        Finalize interview and calculate scores.

        Args:
            session: Database session.
            session_id: The ID of the session to complete.

        Returns:
            Dict containing completion status and aggregated scores.
        """
        logger.info("Completing interview for session: %s", session_id)

        interview_session = session.exec(
            select(InterviewSession)
            .where(InterviewSession.session_id == session_id)
        ).first()

        if not interview_session:
            raise NotFoundError("Interview session not found")

        question_results = session.exec(
            select(QuestionResult)
            .where(QuestionResult.session_id == session_id)
        ).all()

        if not question_results:
            logger.warning(
                "No question results found for session: %s", session_id)
            raise ValidationError("No question results found for this session")

        # Get total questions
        try:
            total_questions = QuestionService.get_total_questions(
                interview_session.role_id
            )
        except Exception as e:
            logger.error("Error getting total questions: %s", e)
            raise

        # Convert ORM models to domain models
        # Calculate aggregated score (directly from ORM models)
        aggregated_score_result = calculate_aggregated_score(
            question_results, total_questions
        )

        # Save or update aggregated score
        cls._save_aggregated_score(
            session, interview_session.session_id, aggregated_score_result
        )

        # Mark session as completed
        interview_session.status = InterviewStatus.COMPLETED
        interview_session.completed_at = datetime.utcnow()
        session.add(interview_session)  # Ensure it's in session
        session.commit()

        return {
            "message": "Interview completed successfully",
            "session_id": session_id,
            "recommendation": aggregated_score_result.overall_recommendation,
            "average_score": aggregated_score_result.average_score,
        }

    @staticmethod
    def get_summary(session: Session, session_id: str) -> Dict[str, Any]:
        """
        Retrieve interview summary with question results and aggregated scores.

        Args:
            session: Database session.
            session_id: The session ID to retrieve.

        Returns:
            Dict containing the full summary.
        """
        interview_session = session.exec(
            select(InterviewSession)
            .where(InterviewSession.session_id == session_id)
        ).first()

        if not interview_session:
            raise NotFoundError("Session not found")

        question_results = session.exec(
            select(QuestionResult)
            .where(QuestionResult.session_id == session_id)
        ).all()

        results = [InterviewMapper.to_dict(qr) for qr in question_results]

        # Get aggregated score if exists
        aggregated_score = session.exec(
            select(AggregatedScore)
            .where(AggregatedScore.session_id == session_id)
        ).first()

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
    def _get_or_create_session(
        session: Session, session_id: str, candidate_id: int, role_id: str
    ) -> InterviewSession:
        """Helper to get or create an interview session."""
        interview_session = session.exec(
            select(InterviewSession)
            .where(InterviewSession.session_id == session_id)
        ).first()

        if not interview_session:
            interview_session = InterviewSession(
                session_id=session_id,
                candidate_id=candidate_id,
                role_id=role_id,
                status=InterviewStatus.IN_PROGRESS,
            )
            session.add(interview_session)
            session.commit()

        return interview_session

    @staticmethod
    def _save_aggregated_score(
        session: Session, session_id: str, new_score: AggregatedScore
    ) -> None:
        """Save or update the aggregated score in the database."""
        existing_score = session.exec(
            select(AggregatedScore)
            .where(AggregatedScore.session_id == session_id)
        ).first()

        if existing_score:
            existing_score.average_score = new_score.average_score
            existing_score.communication_avg = new_score.communication_avg
            existing_score.relevance_avg = new_score.relevance_avg
            existing_score.logical_thinking_avg = new_score.logical_thinking_avg
            existing_score.pass_rate = new_score.pass_rate
            existing_score.overall_recommendation = new_score.overall_recommendation
            existing_score.questions_answered = new_score.questions_answered
            existing_score.total_questions = new_score.total_questions
            session.add(existing_score)
        else:
            # Ensure session_id is set (new_score might not have it if created in aggregator)
            new_score.session_id = session_id
            session.add(new_score)
