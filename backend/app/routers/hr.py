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
    questions = HRService.generate_questions(
        api_key, data.role_title, data.job_description
    )
    return {"suggested_questions": questions}


@router.post("/save-questions")
async def save_questions_api(data: SaveQuestionsRequest) -> Dict[str, str]:
    """Save approved interview questions to JSON database."""
    return HRService.save_role_questions(
        data.role_id, data.role_title, data.questions
    )


@router.get("/roles")
def get_roles() -> list[Dict[str, str]]:
    """Get all job roles."""
    return HRService.get_all_roles()


@router.get("/roles/{role_id}")
def get_role_details(role_id: str) -> Dict[str, Any]:
    """Get detailed information for a specific role."""
    return RoleService.get_role_by_id(role_id)


@router.put("/roles/{role_id}/questions")
async def update_role_questions(
    role_id: str,
    data: UpdateQuestionsRequest
) -> Dict[str, str]:
    """Update questions for an existing role."""
    return HRService.update_role_questions(role_id, data.questions)


@router.delete("/roles/{role_id}")
async def delete_role(role_id: str) -> Dict[str, str]:
    """Delete a role completely."""
    return HRService.delete_role(role_id)
