"""
Score aggregation logic for AI Interview system.

This module provides functions to:
- Calculate aggregated scores from individual question results
- Generate overall recommendations based on performance metrics
"""
from typing import List

from app.domain.models import AggregatedScore, QuestionResult


def calculate_aggregated_score(
    question_results: List[QuestionResult],
    total_questions: int
) -> AggregatedScore:
    """
    Calculate aggregated scores from a list of question results.

    Args:
        question_results: List of QuestionResult domain models
        total_questions: Total number of questions for the role

    Returns:
        AggregatedScore: Domain model containing aggregated metrics
    """
    if not question_results:
        return AggregatedScore(
            total_score=0.0,
            communication_avg=0.0,
            relevance_avg=0.0,
            logical_thinking_avg=0.0,
            pass_rate=0.0,
            overall_recommendation="Fail",
            questions_answered=0,
            total_questions=total_questions
        )

    num_questions = len(question_results)

    # Calculate averages from domain models
    total_score = (
        sum(q.evaluation.scores.total for q in question_results) / num_questions
    )
    communication_avg = (
        sum(q.evaluation.scores.communication for q in question_results) /
        num_questions
    )
    relevance_avg = (
        sum(q.evaluation.scores.relevance for q in question_results) /
        num_questions
    )
    logical_thinking_avg = (
        sum(q.evaluation.scores.logical_thinking for q in question_results) /
        num_questions
    )

    # Calculate pass rate (percentage)
    passed_questions = sum(
        1 for q in question_results if q.evaluation.pass_prediction
    )
    pass_rate = (passed_questions / num_questions) * 100

    # Generate recommendation
    recommendation = generate_recommendation(total_score, pass_rate)

    return AggregatedScore(
        total_score=round(total_score, 2),
        communication_avg=round(communication_avg, 2),
        relevance_avg=round(relevance_avg, 2),
        logical_thinking_avg=round(logical_thinking_avg, 2),
        pass_rate=round(pass_rate, 2),
        overall_recommendation=recommendation,
        questions_answered=num_questions,
        total_questions=total_questions
    )


def generate_recommendation(avg_score: float, pass_rate: float) -> str:
    """
    Generate overall recommendation based on average score AND pass rate.

    Args:
        avg_score: Average total score (0-10 scale)
        pass_rate: Percentage of passed questions (0-100)

    Returns:
        Recommendation string: "Strong Pass", "Pass", "Review", or "Fail"

    Scoring criteria (BOTH metrics must meet threshold):
    - Strong Pass: avg_score >= 8.0 (80%) AND pass_rate >= 80%
    - Pass: avg_score >= 6.0 (60%) AND pass_rate >= 60%
    - Review: avg_score >= 4.0 (40%) OR pass_rate >= 40%
    - Fail: avg_score < 4.0 (below 40%) AND pass_rate < 40%
    """
    # Convert 0-10 scale to percentage for comparison
    score_percentage = (avg_score / 10) * 100

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
