"""
HR Management API routes.

Provides endpoints for HR users to:
- Generate interview questions from job descriptions
- Save approved questions to database
- Retrieve list of all job roles
- Update questions for existing roles
- Delete roles
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.schemas import JDInput, SaveQuestionsRequest, UpdateQuestionsRequest
from app.services import HRService
from app.services.core.role_service import RoleService
from app.dependencies import get_api_key

router = APIRouter(
    prefix="/hr",
    tags=["HR Management"]
)


@router.post("/generate-questions")
async def generate_questions_api(
    data: JDInput,
    api_key: str = Depends(get_api_key)
) -> Dict[str, Any]:
    """Generate interview questions from job description using AI."""
    # This remains blocking for now, or could be wrapped in threadpool if slow.
    questions = HRService.generate_questions(
        api_key, data.role_title, data.job_description
    )
    return {"suggested_questions": questions}


@router.post("/save-questions")
async def save_questions_api(
    data: SaveQuestionsRequest,
    session: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """Save approved interview questions to JSON database."""
    return await HRService.save_role_questions(
        session, data.role_id, data.role_title, data.questions
    )


@router.get("/roles")
async def get_roles(
    session: AsyncSession = Depends(get_db)
) -> list[Dict[str, Any]]:
    """Get all job roles."""
    return await HRService.get_all_roles(session)


@router.get("/roles/{role_id}")
async def get_role_details(
    role_id: str,
    session: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get detailed information for a specific role."""
    return await RoleService.get_role_by_id(session, role_id)


@router.put("/roles/{role_id}/questions")
async def update_role_questions(
    role_id: str,
    data: UpdateQuestionsRequest,
    session: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """Update questions for an existing role."""
    return await HRService.update_role_questions(session, role_id, questions=data.questions, title=data.title)


@router.delete("/roles/{role_id}")
async def delete_role(
    role_id: str,
    session: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """Delete a role completely."""
    return await HRService.delete_role(session, role_id)
