"""
PDF Report Generator for AI Interview System.

Generates professional PDF reports containing:
- Candidate information
- Score summary
- Detailed question-by-question results with feedback
"""
from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.schemas import InterviewReportResponse


from app.config.logging_config import get_logger

logger = get_logger(__name__)


def _register_thai_fonts():
    """Register Thai-compatible fonts for PDF generation."""
    try:
        # Try to register Leelawadee UI from Windows Fonts
        windows_fonts = Path("C:/Windows/Fonts")
        leelawadee_regular = windows_fonts / "LeelawUI.ttf"
        leelawadee_bold = windows_fonts / "LeelaUIb.ttf"

        if leelawadee_regular.exists():
            pdfmetrics.registerFont(
                TTFont('ThaiFont', str(leelawadee_regular)))
            if leelawadee_bold.exists():
                pdfmetrics.registerFont(
                    TTFont('ThaiFont-Bold', str(leelawadee_bold)))
            return True
    except (OSError, TTFError) as e:
        logger.warning(f"Could not register Thai fonts: {e}")
    return False


# Register fonts at module import time.
_THAI_FONT_AVAILABLE = _register_thai_fonts()

# Font names to use.
if _THAI_FONT_AVAILABLE:
    FONT_REGULAR = 'ThaiFont'
    FONT_BOLD = 'ThaiFont-Bold'
else:
    FONT_REGULAR = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'


def generate_pdf_report(report: InterviewReportResponse) -> bytes:
    """
    Generate a PDF report from interview data.

    Args:
        report: InterviewReportResponse containing all interview data

    Returns:
        bytes: PDF file content as bytes
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=1 * inch,
        bottomMargin=0.75 * inch
    )

    # Container for PDF elements
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=FONT_BOLD,
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName=FONT_BOLD,
        fontSize=16,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12
    )

    # Normal style with Thai font
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName=FONT_REGULAR
    )

    # Title
    story.append(Paragraph("AI Interview Report", title_style))
    story.append(Spacer(1, 0.2 * inch))

    # Candidate Information Section
    story.append(Paragraph("Candidate Information", heading_style))

    candidate_data = [
        ['Name:', report.candidate.name],
        ['Email:', report.candidate.email or 'N/A'],
        ['Session ID:', report.candidate.session_id],
        ['Role:', report.candidate.role_id],
        ['Interview Date:', report.candidate.interview_date],
    ]

    candidate_table = Table(
        candidate_data,
        colWidths=[1.5 * inch, 4.5 * inch]
    )
    candidate_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), FONT_BOLD),
        ('FONTNAME', (1, 0), (1, -1), FONT_REGULAR),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(candidate_table)
    story.append(Spacer(1, 0.3 * inch))

    # Score Summary Section
    if report.aggregated_score:
        story.append(Paragraph("Score Summary", heading_style))

        agg = report.aggregated_score

        # Determine recommendation color
        rec_color = colors.green
        if agg.overall_recommendation == "Fail":
            rec_color = colors.red
        elif agg.overall_recommendation == "Review":
            rec_color = colors.orange
        elif agg.overall_recommendation == "Pass":
            rec_color = colors.blue

        score_data = [
            ['Overall Recommendation:', agg.overall_recommendation],
            ['Average Score:', f"{agg.average_score:.2f} / 10"],
            ['Communication Score:', f"{agg.communication_avg:.2f} / 10"],
            ['Relevance Score:', f"{agg.relevance_avg:.2f} / 10"],
            ['Logical Thinking Score:',
                f"{agg.logical_thinking_avg:.2f} / 10"],
            ['Pass Rate:', f"{agg.pass_rate:.1f}%"],
            [
                'Questions Answered:',
                f"{agg.questions_answered} / {agg.total_questions}"
            ],
        ]

        score_table = Table(score_data, colWidths=[2 * inch, 4 * inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('BACKGROUND', (1, 0), (1, 0), rec_color),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('TEXTCOLOR', (1, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), FONT_BOLD),
            ('FONTNAME', (1, 0), (1, 0), FONT_BOLD),
            ('FONTNAME', (1, 1), (1, -1), FONT_REGULAR),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 0.3 * inch))

    # Question Details Section
    story.append(Paragraph("Question-by-Question Analysis", heading_style))
    story.append(Spacer(1, 0.1 * inch))

    for idx, q in enumerate(report.questions, 1):
        # Question header
        q_header_style = ParagraphStyle(
            'QuestionHeader',
            parent=styles['Heading3'],
            fontName=FONT_BOLD,
            fontSize=12,
            textColor=colors.HexColor('#0066cc'),
            spaceAfter=6
        )
        story.append(Paragraph(f"Question {idx}", q_header_style))

        # Question text
        question_text = f"<b>Q:</b> {q.question}"
        story.append(Paragraph(question_text, normal_style))
        story.append(Spacer(1, 0.1 * inch))

        # Scores table
        q_scores_data = [
            ['Communication', 'Relevance', 'Logical Thinking', 'Average', 'Pass'],
            [
                f"{q.communication_score}/10",
                f"{q.relevance_score}/10",
                f"{q.logical_thinking_score}/10",
                f"{q.average_score}/10",
                "PASS" if q.pass_prediction else "FAIL"
            ]
        ]

        q_scores_table = Table(q_scores_data, colWidths=[1.1 * inch] * 5)
        q_scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
            ('FONTNAME', (0, 1), (-1, 1), FONT_REGULAR),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            (
                'BACKGROUND',
                (4, 1),
                (4, 1),
                colors.lightgreen if q.pass_prediction
                else colors.lightcoral
            ),
        ]))
        story.append(q_scores_table)
        story.append(Spacer(1, 0.1 * inch))

        # Transcript
        if q.transcript:
            story.append(Paragraph("<b>Answer:</b>", normal_style))
            transcript_style = ParagraphStyle(
                'Transcript',
                parent=styles['Normal'],
                fontName=FONT_REGULAR,
                fontSize=9,
                leftIndent=20,
                textColor=colors.HexColor('#555555')
            )
            story.append(Paragraph(q.transcript, transcript_style))
            story.append(Spacer(1, 0.1 * inch))

        # Feedback
        if q.feedback:
            feedback = q.feedback
            if isinstance(feedback, dict):
                if 'strengths' in feedback and feedback['strengths']:
                    strengths_text = (
                        f"<b>Strengths:</b> {feedback['strengths']}"
                    )
                    story.append(Paragraph(strengths_text, normal_style))
                if 'weaknesses' in feedback and feedback['weaknesses']:
                    weaknesses_text = (
                        f"<b>Areas for Improvement:</b> "
                        f"{feedback['weaknesses']}"
                    )
                    story.append(Paragraph(weaknesses_text, normal_style))
                if 'summary' in feedback and feedback['summary']:
                    summary_text = (
                        f"<b>Summary:</b> {feedback['summary']}"
                    )
                    story.append(Paragraph(summary_text, normal_style))

        story.append(Spacer(1, 0.2 * inch))

        # Add page break after every 2 questions (except the last)
        if idx % 2 == 0 and idx < len(report.questions):
            story.append(PageBreak())

    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
