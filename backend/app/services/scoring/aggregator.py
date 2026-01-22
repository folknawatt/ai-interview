"""
Score aggregation logic for AI Interview system.

This module provides functions to:
- Calculate aggregated scores from individual question results
- Generate overall recommendations based on performance metrics
"""
from typing import List

from app.database.models import AggregatedScore, QuestionResult


def calculate_aggregated_score(
    all_question_results: List[QuestionResult],
    expected_total_questions: int
) -> AggregatedScore:
    """
    Calculate aggregated scores from a list of question results.

    Args:
        all_question_results: List of QuestionResult ORM models
        expected_total_questions: Total number of questions for the role

    Returns:
        AggregatedScore: ORM model containing aggregated metrics (not attached to session)
    """
    if not all_question_results:
        return AggregatedScore(
            average_score=0.0,
            communication_avg=0.0,
            relevance_avg=0.0,
            logical_thinking_avg=0.0,
            pass_rate=0.0,
            overall_recommendation="Fail",
            questions_answered=0,
            total_questions=expected_total_questions
        )

    # Filter for actually answered questions (e.g. valid score or transcript)
    # We use transcript as the flag for "answered"
    answered_results = [
        q for q in all_question_results if q.transcript is not None]

    num_answered = len(answered_results)

    # If no questions answered, return 0 scores but keep total_questions info
    if num_answered == 0:
        return AggregatedScore(
            average_score=0.0,
            communication_avg=0.0,
            relevance_avg=0.0,
            logical_thinking_avg=0.0,
            pass_rate=0.0,
            overall_recommendation="Fail",
            questions_answered=0,
            total_questions=expected_total_questions
        )

    # Calculate averages based on ANSWERED questions only
    communication_avg = (
        sum(q.communication_score for q in answered_results) / num_answered
    )
    relevance_avg = (
        sum(q.relevance_score for q in answered_results) / num_answered
    )
    logical_thinking_avg = (
        sum(q.logical_thinking_score for q in answered_results) / num_answered
    )

    # Calculate total_score as average of the three category averages
    avg_score = (
        communication_avg + relevance_avg + logical_thinking_avg
    ) / 3

    # Calculate pass rate
    # Note: pass_prediction implies the question was evaluated
    passed_questions_count = sum(
        1 for q in answered_results if q.pass_prediction
    )
    # Pass rate is usually based on answered questions
    passed_percentage = (passed_questions_count / num_answered) * 100

    # Generate recommendation
    recommendation = generate_recommendation(avg_score, passed_percentage)

    return AggregatedScore(
        average_score=round(avg_score, 2),
        communication_avg=round(communication_avg, 2),
        relevance_avg=round(relevance_avg, 2),
        logical_thinking_avg=round(logical_thinking_avg, 2),
        pass_rate=round(passed_percentage, 2),
        overall_recommendation=recommendation,
        questions_answered=num_answered,
        total_questions=expected_total_questions
    )


def generate_recommendation(avg_score: float, pass_rate: float) -> str:
    """
    Generate overall recommendation based on average score AND pass rate.

    Args:
        avg_score: Average total score (1-5 scale)
        pass_rate: Percentage of passed questions (0-100)

    Returns:
        Recommendation string: "Strong Pass", "Pass", "Review", or "Fail"
    """
    # Convert 1-5 scale to percentage for comparison
    score_percentage = (avg_score / 5) * 100

    # Both metrics must meet threshold for Strong Pass/Pass
    if score_percentage >= 80 and pass_rate >= 80:
        return "Strong Pass"
    elif score_percentage >= 60 and pass_rate >= 60:
        return "Pass"
    # Either metric can trigger Review (needs attention)
    elif score_percentage >= 40 or pass_rate >= 40:
        return "Review"
    else:
        return "Fail"
