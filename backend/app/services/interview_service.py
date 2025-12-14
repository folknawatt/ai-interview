"""
Interview Service.
Encapsulates business logic for candidate interviews, including:
- Candidate management
- Answer processing (Video -> Audio -> Transcript -> AI Evaluation)
- Scoring and Summaries
"""
import os
import logging
import asyncio
import uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.domain.scoring.evaluator import evaluate_candidate
from app.adapters.ai.typhoon_asr import extract_audio, transcribe_audio
from app.domain.scoring.aggregator import calculate_aggregated_score
from app.exceptions import NotFoundError, ValidationError
from app.database.models import Candidate, QuestionResult, AggregatedScore
from app.services.candidate_service import CandidateService
from app.services.question_service import QuestionService
from app.services.storage_service import StorageService
from app.services.mappers import InterviewMapper
from app.config.settings import settings


logger = logging.getLogger(__name__)

TEMP_DIR = Path(settings.temp_storage_dir)


class InterviewService:
    """Service class for handling interview business logic."""

    @staticmethod
    async def process_answer(
        session: Session,
        api_key: str,
        file: UploadFile,
        question: str,
        candidate_data: Dict[str, str]
    ) -> Dict[str, Any]:
        """Upload video, extract audio, transcribe, and evaluate."""
        session_id = candidate_data["session_id"]
        role_id = candidate_data["role_id"]
        name = candidate_data["name"]
        email = candidate_data.get("email")

        # Get or create candidate
        candidate = CandidateService.get_or_create(
            session, session_id, name, email, role_id
        )

        file_location = None
        audio_path = None

        try:
            # Save video file (renaming handled by StorageService or assumed safe)
            # Ideally we'd set file.filename to UUID before passing, or StorageService generates it.
            # Current StorageService implementation uses file.filename directly.
            # So we should rename it here as we did before.
            file_ext = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file.filename = unique_filename

            file_location = await StorageService.save_upload(file, TEMP_DIR)

            # Process video
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as pool:
                audio_path = await loop.run_in_executor(
                    pool, extract_audio, str(file_location)
                )
                transcript = await loop.run_in_executor(
                    pool, transcribe_audio, audio_path
                )
                evaluation = await loop.run_in_executor(
                    pool, evaluate_candidate, api_key, question, transcript
                )

            # Cleanup
            StorageService.cleanup([file_location, audio_path])

            # Save result using Mapper
            question_result = InterviewMapper.to_orm_question_result(
                candidate.id, question, transcript, evaluation
            )
            session.add(question_result)
            session.commit()
            session.refresh(question_result)

            return InterviewMapper.to_dict(question_result)

        except Exception as e:
            # Cleanup files before re-raising
            StorageService.cleanup([file_location, audio_path])
            logger.error("Error processing answer: %s", e)
            raise

    @staticmethod
    def complete_interview(session: Session, session_id: str) -> Dict[str, Any]:
        """Finalize interview and calculate scores."""
        candidate = (
            session.query(Candidate)
            .filter(Candidate.session_id == session_id)
            .first()
        )
        if not candidate:
            raise NotFoundError("Candidate session not found")

        question_results = (
            session.query(QuestionResult)
            .filter(QuestionResult.candidate_id == candidate.id)
            .all()
        )

        if not question_results:
            raise ValidationError("No question results found for this session")

        # Get total questions
        total_questions = QuestionService.get_total_questions(
            candidate.role_id
        )

        # Convert ORM models to domain models first
        domain_question_results = [
            InterviewMapper.to_domain_question_result(qr)
            for qr in question_results
        ]

        # Calculate aggregated score using domain models
        aggregated_domain = calculate_aggregated_score(
            domain_question_results,
            total_questions
        )

        # Save or update aggregated score
        existing_score = (
            session.query(AggregatedScore)
            .filter(AggregatedScore.candidate_id == candidate.id)
            .first()
        )

        if existing_score:
            existing_score.total_score = aggregated_domain.total_score
            existing_score.communication_avg = aggregated_domain.communication_avg
            existing_score.relevance_avg = aggregated_domain.relevance_avg
            existing_score.quality_avg = aggregated_domain.quality_avg
            existing_score.pass_rate = aggregated_domain.pass_rate
            existing_score.overall_recommendation = aggregated_domain.overall_recommendation
            existing_score.questions_answered = aggregated_domain.questions_answered
            existing_score.total_questions = aggregated_domain.total_questions
        else:
            aggregated_score = AggregatedScore(
                candidate_id=candidate.id,
                total_score=aggregated_domain.total_score,
                communication_avg=aggregated_domain.communication_avg,
                relevance_avg=aggregated_domain.relevance_avg,
                quality_avg=aggregated_domain.quality_avg,
                pass_rate=aggregated_domain.pass_rate,
                overall_recommendation=aggregated_domain.overall_recommendation,
                questions_answered=aggregated_domain.questions_answered,
                total_questions=aggregated_domain.total_questions
            )
            session.add(aggregated_score)

        # Mark candidate as completed
        CandidateService.mark_completed(session, session_id)

        return {
            "message": "Interview completed successfully",
            "session_id": session_id,
            "recommendation": aggregated_domain.overall_recommendation,
            "total_score": aggregated_domain.total_score
        }

    @staticmethod
    def get_summary(session: Session, session_id: str) -> Dict[str, Any]:
        """Retrieve interview summary with question results and aggregated scores."""
        candidate = (
            session.query(Candidate)
            .filter(Candidate.session_id == session_id)
            .first()
        )
        if not candidate:
            raise NotFoundError("Session not found")

        question_results = (
            session.query(QuestionResult)
            .filter(QuestionResult.candidate_id == candidate.id)
            .all()
        )

        results = [
            InterviewMapper.to_dict(qr)
            for qr in question_results
        ]

        # Get aggregated score if exists
        aggregated_score = (
            session.query(AggregatedScore)
            .filter(AggregatedScore.candidate_id == candidate.id)
            .first()
        )

        aggregated_data = None
        if aggregated_score:
            aggregated_data = {
                "total_score": aggregated_score.total_score,
                "communication_avg": aggregated_score.communication_avg,
                "relevance_avg": aggregated_score.relevance_avg,
                "quality_avg": aggregated_score.quality_avg,
                "pass_rate": aggregated_score.pass_rate,
                "overall_recommendation": aggregated_score.overall_recommendation,
                "questions_answered": aggregated_score.questions_answered,
                "total_questions": aggregated_score.total_questions
            }

        return {
            "total_questions": len(results),
            "details": results,
            "aggregated_score": aggregated_data
        }
