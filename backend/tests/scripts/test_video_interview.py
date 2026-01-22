"""
Video Interview Test Script

Test script for developers to test the interview API with pre-recorded video files.
Displays evaluation scores and feedback in a formatted output.

Usage:
    1. Edit the CONFIG section below with your values
    2. Run: uv run python scripts/test_video_interview.py
"""
import sys
import uuid
from pathlib import Path

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box


console = Console()


def get_first_question(api_url: str, role_id: str) -> tuple[str, int]:
    """Fetch the first question for a role from the API."""
    url = f"{api_url}/interview/question/{role_id}/0"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    if data.get("status") == "continue":
        return data["question"], data.get("question_id", 0)
    else:
        raise ValueError(f"No questions found for role '{role_id}'")


def upload_video_answer(
    api_url: str,
    video_path: str,
    question: str,
    question_id: int,
    role_id: str,
    candidate_name: str,
) -> dict:
    """Upload video answer to the interview API."""
    url = f"{api_url}/interview/upload-answer"

    # Generate unique session ID
    session_id = f"test_{uuid.uuid4().hex[:8]}"

    # Prepare file and form data
    video_file = Path(video_path)
    if not video_file.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Determine content type
    suffix = video_file.suffix.lower()
    content_types = {
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".avi": "video/avi",
        ".mov": "video/quicktime",
    }
    content_type = content_types.get(suffix, "video/mp4")

    with open(video_path, "rb") as f:
        files = {"file": (video_file.name, f, content_type)}
        data = {
            "question": question,
            "question_id": str(question_id),
            "session_id": session_id,
            "role_id": role_id,
            "candidate_name": candidate_name,
        }
        response = requests.post(url, files=files, data=data, timeout=120)
        response.raise_for_status()
        return response.json()


def display_results(result: dict) -> None:
    """Display evaluation results in a formatted, colorful output."""
    console.print()
    console.rule("[bold blue]📊 Interview Evaluation Results[/bold blue]")
    console.print()

    # Transcript Panel
    transcript = result.get("transcript", "N/A")
    console.print(Panel(
        transcript,
        title="[bold cyan]📝 Transcript[/bold cyan]",
        border_style="cyan"
    ))
    console.print()

    # Scores Table
    evaluation = result.get("evaluation", {})
    scores = evaluation.get("scores", {})

    scores_table = Table(
        title="[bold green]📈 Scores (1-5)[/bold green]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    scores_table.add_column("Category", style="cyan")
    scores_table.add_column("Score", justify="center", style="yellow")
    scores_table.add_column("Level", justify="center")

    def get_level(score: float) -> str:
        if score >= 4.5:
            return "[bold green]Excellent[/bold green]"
        elif score >= 3.5:
            return "[green]Good[/green]"
        elif score >= 2.5:
            return "[yellow]Average[/yellow]"
        elif score >= 1.5:
            return "[orange3]Below Average[/orange3]"
        else:
            return "[red]Poor[/red]"

    score_items = [
        ("Communication", scores.get("communication", 0)),
        ("Relevance", scores.get("relevance", 0)),
        ("Logical Thinking", scores.get("logical_thinking", 0)),
    ]

    for name, score in score_items:
        scores_table.add_row(name, f"{score:.1f}", get_level(score))

    # Add total score if available
    total = scores.get("total")
    if total is not None:
        scores_table.add_row(
            "[bold]TOTAL[/bold]",
            f"[bold]{total:.1f}[/bold]",
            get_level(total)
        )

    console.print(scores_table)
    console.print()

    # Feedback Panel
    feedback = evaluation.get("feedback", {})
    feedback_text = f"""
[bold green]✅ Strengths:[/bold green]
{feedback.get('strengths', 'N/A')}

[bold red]⚠️ Weaknesses:[/bold red]
{feedback.get('weaknesses', 'N/A')}

[bold blue]📋 Summary:[/bold blue]
{feedback.get('summary', 'N/A')}
    """.strip()

    console.print(Panel(
        feedback_text,
        title="[bold yellow]💬 Feedback[/bold yellow]",
        border_style="yellow"
    ))
    console.print()

    # Pass Prediction
    pass_pred = evaluation.get("pass_prediction", None)
    if pass_pred is not None:
        if pass_pred:
            console.print(Panel(
                "[bold green]✅ PASSED[/bold green] - Candidate meets the criteria",
                border_style="green"
            ))
        else:
            console.print(Panel(
                "[bold red]❌ NOT PASSED[/bold red] - Candidate needs improvement",
                border_style="red"
            ))

    console.print()


def main(
    video_path: str,
    role_id: str,
    candidate_name: str,
    api_url: str,
) -> None:
    """Main function to run the video interview test."""
    console.print()
    console.rule("[bold purple]🎬 Video Interview Test[/bold purple]")
    console.print()

    # Step 1: Get question
    console.print("[cyan]📋 Fetching question from API...[/cyan]")
    try:
        question, question_id = get_first_question(api_url, role_id)
        console.print(f"[green]✓[/green] Question: {question[:80]}...")
    except Exception as e:
        console.print(f"[red]✗ Failed to get question: {e}[/red]")
        sys.exit(1)

    # Step 2: Upload video
    console.print()
    console.print(f"[cyan]📤 Uploading video: {video_path}[/cyan]")
    try:
        result = upload_video_answer(
            api_url=api_url,
            video_path=video_path,
            question=question,
            question_id=question_id,
            role_id=role_id,
            candidate_name=candidate_name,
        )
        console.print("[green]✓ Video uploaded and processed![/green]")
    except FileNotFoundError as e:
        console.print(f"[red]✗ {e}[/red]")
        sys.exit(1)
    except requests.RequestException as e:
        console.print(f"[red]✗ API Error: {e}[/red]")
        sys.exit(1)

    # Step 3: Display results
    display_results(result)


if __name__ == "__main__":
    # ========== CONFIG - แก้ไขค่าตรงนี้ ==========
    # <-- ใส่ path ไฟล์ video ที่ต้องการทดสอบ
    VIDEO_PATH = r"D:\ai-interview\backend\scripts\snaptik_7318925278326082821_v2.mp4"
    ROLE_ID = "test_dev"                        # <-- ใส่ role_id ที่ต้องการ
    CANDIDATE_NAME = "Test User"                # <-- ชื่อผู้สมัครทดสอบ
    API_BASE_URL = "http://localhost:8000"      # <-- URL ของ API server
    # =============================================

    main(
        video_path=VIDEO_PATH,
        role_id=ROLE_ID,
        candidate_name=CANDIDATE_NAME,
        api_url=API_BASE_URL,
    )
