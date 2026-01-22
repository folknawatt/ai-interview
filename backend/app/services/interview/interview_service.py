"""
Interview Service.

Encapsulates business logic for candidate interviews, including:
- Candidate management
- Answer processing (Video -> Audio -> Transcript -> AI Evaluation)
- Scoring and Summaries
"""
import asyncio
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import UploadFile
from sqlmodel import Session, select

from app.config.logging_config import get_logger
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
from app.services.core.role_service import RoleService
from app.services.core.storage_service import StorageService

logger = get_logger(__name__)

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
        cleanup_needed = True  # Flag to track if cleanup is needed

        try:
            # Save video file
            file_ext = Path(file.filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file.filename = unique_filename

            file_location = await StorageService.save_upload(file, TEMP_DIR)

            # Fetch role title
            role_title = RoleService.get_role_title(role_id)

            # Process media (Video -> Audio -> Transcript)
            transcript = await MediaService.process_video_to_transcript(
                str(file_location)
            )

            # Evaluate Candidate Answer
            # Run CPU-bound/network-bound synchronous evaluation in a thread
            evaluation = await asyncio.to_thread(
                evaluate_candidate, api_key, question, transcript, role_title
            )

            # Save result using Mapper
            # Logic: Check if snapshot exists first to avoid duplicates
            existing_qr = session.exec(
                select(QuestionResult)
                .where(QuestionResult.session_id == session_id)
                .where(QuestionResult.question == question)
            ).first()

            if existing_qr:
                # Update existing snapshot
                existing_qr.transcript = transcript
                existing_qr.communication_score = evaluation.scores.communication
                existing_qr.relevance_score = evaluation.scores.relevance
                existing_qr.logical_thinking_score = evaluation.scores.logical_thinking
                existing_qr.pass_prediction = evaluation.pass_prediction

                # Feedback needs to be Dict for JSON storage
                existing_qr.feedback = {
                    "strengths": evaluation.feedback.strengths,
                    "weaknesses": evaluation.feedback.weaknesses,
                    "summary": evaluation.feedback.summary
                }

                # question_id is optional, but if provided in form, we might want to ensure it's set
                if question_id != -1:
                    existing_qr.question_id = question_id

                session.add(existing_qr)
                question_result = existing_qr
            else:
                # Fallback: Create new if not found (should not happen in snapshot flow)
                # Note: InterviewMapper.to_orm_question_result handles the mapping internally
                # We need to make sure it also handles the nested object correctly if we use it
                question_result = InterviewMapper.to_orm_question_result(
                    session_id, question_id, question, transcript, evaluation
                )
                session.add(question_result)
            session.commit()
            session.refresh(question_result)

            return InterviewMapper.to_dict(question_result)

        except ValueError as e:
            # Input error (empty transcript or bad format)
            logger.warning("Validation error in process_answer: %s", e)
            raise ValidationError(str(e)) from e

        except ConnectionError as e:
            # External service unavailable
            logger.error("Connection error in process_answer: %s", e)
            raise ServiceUnavailableError(
                "AI Service temporarily unavailable") from e

        except RuntimeError as e:
            # External service error
            logger.error("Runtime error in process_answer: %s", e)
            raise BadGatewayError("AI Service returned an error") from e

        except Exception as e:
            logger.error("Error processing answer: %s", e)
            raise

        finally:
            # Centralized cleanup - always runs regardless of success/failure
            if cleanup_needed and file_location:
                StorageService.cleanup([file_location])

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
        # Using Snapshot Pattern: The number of QuestionResult rows IS the total questions for this session.
        # This naturally handles custom questions added via Resume Upload.
        total_questions = len(question_results)

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
        interview_session.completed_at = datetime.now(timezone.utc)
        session.add(interview_session)  # Ensure it's in session
        session.commit()

        return {
            "message": "Interview completed successfully",
            "session_id": session_id,
            "recommendation": aggregated_score_result.overall_recommendation,
            "average_score": aggregated_score_result.average_score,
        }

    @staticmethod
    def init_session_with_questions(
        session: Session,
        role_id: str,
        questions: list[str],
        candidate_name: str = "Anonymous",
        candidate_email: Optional[str] = None
    ) -> str:
        """
        Initialize a new interview session with specific questions (Snapshot Pattern).
        Creates/Retrieves candidate and persists questions to QuestionResult.
        """
        # 1. Create/Get Candidate
        candidate = CandidateService.get_or_create(
            session, candidate_name, candidate_email)

        # 2. Generate Session ID
        session_id = f"sess_{uuid.uuid4().hex[:12]}"

        # 3. Create Session
        interview_session = InterviewSession(
            session_id=session_id,
            candidate_id=candidate.id,
            role_id=role_id,  # Link to Base Role (e.g., 'marketing')
            status=InterviewStatus.STARTED
        )
        session.add(interview_session)

        # 4. Snapshot Questions to QuestionResult
        for idx, q_text in enumerate(questions):
            # Create QuestionResult with empty status
            qr = QuestionResult(
                session_id=session_id,
                question=q_text,
                communication_score=0.0,
                relevance_score=0.0,
                logical_thinking_score=0.0,
                pass_prediction=False,
                feedback={}
            )
            session.add(qr)

        session.commit()
        return session_id

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

        # CRITICAL: Commit to persist aggregated score to database
        session.commit()
