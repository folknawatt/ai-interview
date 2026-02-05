"""
HR Reporting API routes.

Provides endpoints for HR to:
- List all completed interviews with filtering
- Get detailed interview reports
- Download PDF reports
- View overall statistics
"""
import io
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.services import ReportService
from app.schemas import InterviewReportResponse, ReportListItem

router = APIRouter(
    prefix="/reports",
    tags=["HR Reports"]
)


@router.get("/all", response_model=list[ReportListItem])
async def get_all_reports(
    role_id: Optional[str] = None,
    min_score: Optional[float] = None,
    recommendation: Optional[str] = None,
    search_query: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> list[ReportListItem]:
    """
    List all completed interviews with optional filtering.

    Query Parameters:
    - role_id: Filter by role ID
    - min_score: Minimum total score
    - recommendation: Filter by recommendation (Strong Pass, Pass, Review, Fail)
    - search_query: Search by candidate name
    """
    return await ReportService.get_all_reports(
        db, role_id, min_score, recommendation, search_query
    )


@router.get("/{session_id}", response_model=InterviewReportResponse)
async def get_report_details(
    session_id: str,
    db: AsyncSession = Depends(get_db)
) -> InterviewReportResponse:
    """Get detailed report for a specific interview session."""
    return await ReportService.get_report_details(db, session_id)


@router.get("/{session_id}/pdf")
async def download_pdf_report(session_id: str, db: AsyncSession = Depends(get_db)):
    """Generate and download PDF report for an interview."""
    pdf_buffer = await ReportService.generate_pdf_report(db, session_id)

    # Return as streaming response
    return StreamingResponse(
        io.BytesIO(pdf_buffer),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=interview_report_{session_id}.pdf"
        }
    )


@router.get("/statistics/overview")
async def get_statistics(db: AsyncSession = Depends(get_db)) -> dict:
    """Get overall statistics for all completed interviews."""
    return await ReportService.get_statistics(db)
