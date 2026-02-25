"""HR-related Pydantic schemas.

Schemas for HR endpoints including:
- Job description input
- Question management
"""

from pydantic import BaseModel, Field


class JDInput(BaseModel):
    """Job description input for question generation."""

    role_title: str = Field(..., min_length=1, max_length=200, description="Job role title")
    job_description: str = Field(..., min_length=10, description="Detailed job description")


class SaveQuestionsRequest(BaseModel):
    """Request to save interview questions for a role."""

    role_id: str = Field(..., min_length=1, max_length=100, description="Unique role identifier")
    role_title: str = Field(..., min_length=1, max_length=200, description="Job role title")
    questions: list[str] = Field(..., min_items=1, description="List of interview questions")


class UpdateQuestionsRequest(BaseModel):
    """Request to update interview questions for an existing role."""

    questions: list[str] | None = Field(
        None, min_items=1, description="Updated list of interview questions"
    )
    title: str | None = Field(None, description="Updated job role title")
