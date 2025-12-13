"""
Interview Service.
Encapsulates business logic for candidate interviews, including:
- Candidate management
- Answer processing (Video -> Audio -> Transcript -> AI Evaluation)
- Scoring and Summaries
"""
import os
import uuid
import logging
import asyncio
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any

import aiofiles
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.domain.scoring.evaluator import evaluate_candidate
from app.adapters.ai.typhoon_asr import extract_audio, transcribe_audio
from app.domain.scoring.aggregator import calculate_aggregated_score
from app.exceptions import NotFoundError, ValidationError
from app.database.models import Candidate, QuestionResult, AggregatedScore
from app.domain.models import (
    QuestionResult as DomainQuestionResult,
    Evaluation,
    Score,
    Feedback
)
from app.services.candidate_service import CandidateService
from app.services.question_service import QuestionService
from app.utils.file_ops import cleanup_files
from app.config.settings import settings

logger = logging.getLogger(__name__)

TEMP_DIR = Path(settings.temp_storage_dir)
TEMP_DIR.mkdir(parents=True, exist_ok=True)


class InterviewService:
    """Service class for handling interview business logic."""

    @staticmethod
    def _format_question_result(qr: QuestionResult) -> Dict[str, Any]:
        """Format QuestionResult object to dictionary."""
        return {
            "question": qr.question,
            "transcript": qr.transcript,
            "evaluation": {
                "scores": {
                    "communication": qr.communication_score,
                    "relevance": qr.relevance_score,
                    "quality": qr.quality_score,
                    "total": qr.total_score
                },
                "feedback": qr.feedback,
                "pass_prediction": qr.pass_prediction
            }
        }

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

        # Prepare file paths
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_location = TEMP_DIR / unique_filename
        audio_path = None

        try:
            # Save video file
            async with aiofiles.open(file_location, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)

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
            cleanup_files(file_location, audio_path)

            # Save result (convert domain model to ORM model)
            question_result = QuestionResult(
                candidate_id=candidate.id,
                question=question,
                transcript=transcript,
                communication_score=evaluation.scores.communication,
                relevance_score=evaluation.scores.relevance,
                quality_score=evaluation.scores.quality,
                total_score=evaluation.scores.total,
                feedback={
                    "strengths": evaluation.feedback.strengths,
                    "weaknesses": evaluation.feedback.weaknesses,
                    "summary": evaluation.feedback.summary
                },
                pass_prediction=evaluation.pass_prediction
            )
            session.add(question_result)
            session.commit()
            session.refresh(question_result)

            # Convert domain model to dict for response
            return {
                "question": question,
                "transcript": transcript,
                "evaluation": {
                    "scores": {
                        "communication": evaluation.scores.communication,
                        "relevance": evaluation.scores.relevance,
                        "quality": evaluation.scores.quality,
                        "total": evaluation.scores.total
                    },
                    "feedback": {
                        "strengths": evaluation.feedback.strengths,
                        "weaknesses": evaluation.feedback.weaknesses,
                        "summary": evaluation.feedback.summary
                    },
                    "pass_prediction": evaluation.pass_prediction
                }
            }

        except Exception as e:
            # Cleanup files before re-raising
            cleanup_files(file_location, audio_path)
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
            DomainQuestionResult(
                question=qr.question,
                transcript=qr.transcript,
                evaluation=Evaluation(
                    scores=Score(
                        communication=qr.communication_score,
                        relevance=qr.relevance_score,
                        quality=qr.quality_score,
                        total=qr.total_score
                    ),
                    feedback=Feedback(
                        strengths=qr.feedback.get("strengths", ""),
                        weaknesses=qr.feedback.get("weaknesses", ""),
                        summary=qr.feedback.get("summary", "")
                    ),
                    pass_prediction=qr.pass_prediction
                )
            )
            for qr in question_results
        ]

        # Calculate aggregated score using domain models
        aggregated_domain = calculate_aggregated_score(
            domain_question_results,
            total_questions
        )

        # Save or update aggregated score (convert domain to ORM)
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
            InterviewService._format_question_result(qr)
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
