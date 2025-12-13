"""
Candidate domain model.

Pure domain model representing an interview candidate.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Candidate:
    """
    Domain model representing an interview candidate.

    This represents the core business concept of a candidate,
    independent of database storage or API representation.

    Attributes:
        name: Candidate's full name
        email: Candidate's email address (optional)
        session_id: Unique session identifier for the interview
        role_id: ID of the role being interviewed for
        interview_date: When the interview was conducted
        completed: Whether the interview has been completed
    """

    name: str
    email: str | None
    session_id: str
    role_id: str
    interview_date: datetime
    completed: bool
