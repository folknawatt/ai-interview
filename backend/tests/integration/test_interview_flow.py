"""
Integration tests for interview flow.
"""
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.services.interview_service import InterviewService
from app.schemas.interview import InterviewEvaluationResponse, Scores, Feedback


@patch("app.services.interview_service.extract_audio")
@patch("app.services.interview_service.transcribe_audio")
@patch("app.services.interview_service.evaluate_candidate")
@patch("app.services.candidate_service.CandidateService.get_or_create")
@patch("app.services.storage_service.StorageService.save_upload")
@patch("app.services.storage_service.StorageService.cleanup")
def test_upload_answer_flow(
    mock_cleanup,
    mock_save_upload,
    mock_get_or_create_candidate,
    mock_evaluate,
    mock_transcribe,
    mock_extract,
    client: TestClient,
    db_session
):
    """Test the full upload answer flow with mocked AI and storage."""
    # Setup mocks
    mock_extract.return_value = "dummy_audio.wav"
    mock_transcribe.return_value = "This is a test answer."
    mock_evaluate.return_value = InterviewEvaluationResponse(
        scores=Scores(communication=8.0, relevance=9.0,
                      logical_thinking=8.5, total=8.5),
        feedback=Feedback(strengths="Good", weaknesses="None", summary="Okay"),
        reasoning="Good reasoning",
        pass_prediction=True
    )

    # Mock candidate
    mock_candidate = MagicMock()
    mock_candidate.id = 1
    mock_candidate.session_id = "test-session-123"
    mock_get_or_create_candidate.return_value = mock_candidate

    # Mock storage
    mock_save_upload.return_value = "path/to/video.mp4"

    # Prepare input data
    files = {"file": ("test_video.mp4", b"fake video content", "video/mp4")}
    data = {
        "question": "Tell me about yourself",
        "session_id": "test-session-123",
        "role_id": "role-1",
        "candidate_name": "John Doe",
        "candidate_email": "john@example.com"
    }

    # Note: We depend on Main API or Router to call InterviewService.process_answer
    # But since we are testing via client, we hit the endpoint.
    # We need to make sure the endpoint uses key 'api_key' dependency or we provide it.
    # The router expects api_key header? No, Depends(get_api_key) implies header.
    # In .env.example/settings, is there a default API key?

    # Let's check dependency in router.
    # router post "/upload-answer"

    response = client.post(
        "/interview/upload-answer",
        files=files,
        data=data,
        # Assuming get_api_key requires this
        headers={"X-API-Key": "test-api-key"}
    )

    # In conftest.py we didn't override get_api_key, so it might fail if real check is there.
    # Let's assume we need to mock get_api_key or provide one.
    # If app.dependencies.get_api_key checks env var, we might need to set it.

    # Assertions
    if response.status_code != 200:
        print(response.json())

    assert response.status_code == 200
    res_json = response.json()
    assert res_json["transcript"] == "This is a test answer."
    assert res_json["evaluation"]["scores"]["total"] == 8.5

    # Verify mocks called
    mock_save_upload.assert_called_once()
    mock_extract.assert_called_once()
    mock_transcribe.assert_called_once()
    mock_evaluate.assert_called_once()
    mock_cleanup.assert_called_once()
