"""
Question result domain model.

Pure domain model representing the result of answering a single interview question.
"""
from dataclasses import dataclass

from .evaluation import Evaluation


@dataclass
class QuestionResult:
    """
    Domain model representing a candidate's answer to a single question.

    This combines the question, the candidate's transcribed answer,
    and the evaluation results.

    Attributes:
        question: The interview question text
        transcript: Transcribed answer from the candidate (may be None)
        evaluation: AI evaluation of the answer
    """

    question: str
    transcript: str | None
    evaluation: Evaluation
