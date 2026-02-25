# API Documentation

## 🌐 Base URL

- **Development:** `http://localhost:8000`
- **Production:** `https://your-domain.com/api`

## 🔐 Authentication

The system utilizes JWT Tokens stored in HttpOnly Cookies. There is no need to manually append tokens to requests.

### Core Endpoints

- `POST /auth/login`: Authenticate user and receive cookies.
- `POST /auth/logout`: Clear authentication cookies.
- `GET /auth/me`: Retrieve current user profile.
- `POST /auth/register`: Register a new user (Admin only).

## 👥 HR Endpoints

- `POST /hr/generate-questions`: Generate AI-powered questions for a specific role.
- `GET /hr/roles`: Retrieve all available job roles.
- `GET /hr/roles/{role_id}`: Retrieve details for a specific role.
- `POST /hr/save-questions`: Save finalized questions for a job role.
- `PUT /hr/roles/{role_id}/questions`: Update or reorder existing questions.
- `DELETE /hr/roles/{role_id}`: Delete a job role.

## 🎤 Interview Endpoints (Candidate)

- `POST /interview/upload-pdf`: Upload a candidate's Resume (PDF) to generate personalized questions and initialize a session.
- `GET /interview/session/{session_id}/question/{index}`: Retrieve the question at a specific index (supports pre-fetching).
- `POST /interview/upload-answer`: Upload an answer video for real-time AI evaluation.
- `POST /interview/complete/{session_id}`: Finalize the interview session and compute aggregate scores.
- `GET /interview/summary/{session_id}`: Retrieve the comprehensive evaluation results of a completed session.

## 🔊 Text-to-Speech (TTS) Endpoints

- `POST /tts/generate`: Trigger audio generation from text.
- `GET /tts/audio/{filename}`: Retrieve the generated audio file.

## 📊 Reporting & Analytics

- `GET /reports/all`: Retrieve all interview sessions (supports filtering).
- `GET /reports/{session_id}`: Fetch detailed evaluation results for a specific session.
- `GET /reports/{session_id}/pdf`: Download the session evaluation report as a PDF.
- `GET /reports/statistics/overview`: Fetch aggregated system statistics.

## ⚠️ Error Handling

- `400 Bad Request`: Invalid request payload or parameters.
- `404 Not Found`: Requested resource does not exist.
- `500 Internal Server Error`: Unexpected server malfunction.

> 💡 **Tip:** Explore and test the API interactively via Swagger UI at `http://localhost:8000/docs` (when running locally).
