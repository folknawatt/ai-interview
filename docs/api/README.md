# API Documentation

## Base URL

**Development:** `http://localhost:8000`  
**Production:** `https://your-domain.com/api`

## Authentication

Authentication is handled via JWT tokens stored in HttpOnly cookies. There is no need to manually attach tokens to requests, as the browser handles cookies automatically.

### Login

Authenticate a user and set strict HttpOnly cookies.

**Endpoint:** `POST /auth/login`

**Content-Type:** `application/x-www-form-urlencoded`

**Form Data:**

- `username`: User's username
- `password`: User's password

**Response:** `200 OK` (with Set-Cookie headers)

```json
{
  "access_token": "",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin",
    "full_name": "System Admin"
  }
}
```

### Logout

Clear authentication cookies.

**Endpoint:** `POST /auth/logout`

**Response:** `200 OK`

### Get Current User

Get information about the currently logged-in user.

**Endpoint:** `GET /auth/me`

**Response:** `200 OK`

### Register User

Register a new user. Restricted to Admins.

**Endpoint:** `POST /auth/register`

**Request Body:**

```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "New User",
  "role": "hr"
}
```

**Response:** `200 OK`

### Initialize Admin

Initialize the default admin user. Only works if no admin exists.

**Endpoint:** `POST /auth/init-admin`

**Response:** `200 OK`

## HR Endpoints

### Generate Questions

Generate AI-powered interview questions for a specific role.

**Endpoint:** `POST /hr/generate-questions`

**Request Body:**

```json
{
  "role": "Software Engineer",
  "level": "senior",
  "count": 5,
  "focus_areas": ["algorithms", "system design"]
}
```

**Response:** `200 OK`

```json
{
  "questions": [
    {
      "id": "q1",
      "text": "Explain how you would design a distributed caching system",
      "category": "system design",
      "difficulty": "hard"
    }
  ],
  "role": "Software Engineer",
  "generated_at": "2025-12-09T01:00:00Z"
}
```

],
"role": "Software Engineer",
"generated_at": "2025-12-09T01:00:00Z"
}

````

### Delete Role

Delete a role completely.

**Endpoint:** `DELETE /hr/roles/{role_id}`

**Response:** `200 OK`

```json
{
  "status": "success",
  "message": "Role deleted successfully"
}
````

### List Roles

Get all available job roles.

**Endpoint:** `GET /hr/roles`

**Response:** `200 OK`

```json
{
  "roles": [
    {
      "id": "role1",
      "name": "Software Engineer",
      "description": "Backend development role",
      "created_at": "2025-12-01T00:00:00Z"
    }
  ]
}
```

### Get Role Details

Get detailed information for a specific role.

**Endpoint:** `GET /hr/roles/{role_id}`

**Response:** `200 OK`

```json
{
  "id": "role1",
  "name": "Software Engineer",
  "description": "Backend development role",
  "questions": [
    {
      "id": "q1",
      "content": "Question text..."
    }
  ]
}
```

### Save Questions

Save approved questions for a role.

**Endpoint:** `POST /hr/save-questions`

**Request Body:**

```json
{
  "role_id": "role123",
  "role_title": "Software Engineer",
  "questions": ["Question 1", "Question 2"]
}
```

**Response:** `200 OK`

```json
{
  "status": "success",
  "message": "Saved questions for Software Engineer"
}
```

### Update Questions

Update or reorder questions for an existing role.

**Endpoint:** `PUT /hr/roles/{role_id}/questions`

**Request Body:**

```json
{
  "title": "Senior Software Engineer",
  "questions": ["New Question 1", "New Question 2"]
}
```

**Response:** `200 OK`

## Interview Endpoints

### Upload PDF Resume (Snapshot Flow)

Upload a candidate's resume (PDF) to generate custom questions and initialize an interview session. Default flow.

**Endpoint:** `POST /interview/upload-pdf`

**Content-Type:** `multipart/form-data`

**Form Data:**

- `file`: PDF file
- `role_id`: Role ID
- `candidate_name`: Candidate's name
- `candidate_email`: Candidate's email (optional)

**Response:** `200 OK`

```json
{
  "session_id": "sess_12345",
  "role_id": "role_1",
  "questions": ["Base question 1", "Base question 2", "Custom question from resume 1", "Custom question from resume 2"]
}
```

### Get Session Question

Get a question for an active interview session from the frozen snapshot.

**Endpoint:** `GET /interview/session/{session_id}/question/{index}`

**Query Parameters:**

- `skip_tts`: `true` or `false` (default: `false`) - Skip audio generation for pre-fetching.

**Response:** `200 OK`

```json
{
  "question_id": 1,
  "question": "Tell me about yourself.",
  "audio_path": "/audio/sess_12345_0.mp3",
  "total_questions": 5,
  "current_index": 0
}
```

### Upload Answer & Analyze

Upload a video answer for a specific question and immediately trigger AI analysis.

**Endpoint:** `POST /interview/upload-answer`

**Content-Type:** `multipart/form-data`

**Form Data:**

- `file`: Video file (webm/mp4)
- `question`: Question text
- `question_id`: Question ID (index)
- `session_id`: Session ID
- `role_id`: Role ID
- `candidate_name`: Candidate Name
- `candidate_email`: Candidate Email

**Response:** `200 OK`

```json
{
  "id": "result_123",
  "session_id": "sess_12345",
  "question": "Tell me about yourself",
  "transcript": "I am a software engineer...",
  "communication_score": 85.0,
  "relevance_score": 90.0,
  "logical_thinking_score": 88.0,
  "pass_prediction": true,
  "feedback": {
    "strengths": ["Clear communication"],
    "weaknesses": ["Could be more concise"],
    "summary": "Good introduction."
  },
  "video_url": "/videos/uuid.webm"
}
```

### Complete Interview

Finalize the interview session and calculate aggregated scores.

**Endpoint:** `POST /interview/complete/{session_id}`

**Response:** `200 OK`

```json
{
  "message": "Interview completed successfully",
  "session_id": "sess_12345",
  "recommendation": "Strong Pass",
  "average_score": 88.5
}
```

### Get Interview Summary

Get full details and results of a completed interview.

**Endpoint:** `GET /interview/summary/{session_id}`

**Response:** `200 OK`

```json
{
  "total_questions": 5,
  "details": [ ...list of question results... ],
  "aggregated_score": {
    "average_score": 88.5,
    "communication_avg": 85.0,
    "relevance_avg": 90.0,
    "logical_thinking_avg": 90.5,
    "pass_rate": 100.0,
    "overall_recommendation": "Strong Pass"
  }
}
```

## TTS Endpoints

### Generate Speech

Convert text to speech.

**Endpoint:** `POST /tts/generate`

**Request Body:**

```json
{
  "text": "What is your experience with distributed systems?",
  "voice": "en-US-JennyNeural",
  "format": "mp3"
}
```

**Response:** `200 OK`

```json
{
  "audio_url": "/tts/audio/abc123.mp3",
  "duration": 5.2,
  "format": "mp3"
}
```

### Get Audio File

Retrieve a generated audio file.

**Endpoint:** `GET /tts/audio/{filename}`

**Response:** Audio file stream (audio/mpeg)

## Reports Endpoints

### List Reports

List all completed interview sessions with optional filtering.

**Endpoint:** `GET /reports/all`

**Query Parameters:**

- `role_id`: Filter by role
- `min_score`: Filter by minimum score
- `recommendation`: Filter by recommendation (Strong Pass, Pass, Review, Fail)
- `search_query`: Search by candidate name

### Get Report Details

Get full details of a specific interview session.

**Endpoint:** `GET /reports/{session_id}`

### Download PDF

Download a PDF version of the interview report.

**Endpoint:** `GET /reports/{session_id}/pdf`

### Statistics

Get overall platform statistics.

**Endpoint:** `GET /reports/statistics/overview`

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request

```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found

```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error",
  "error": "Detailed error message"
}
```

## Rate Limiting

Currently no rate limiting is implemented. Should be added before production.

## Interactive Documentation

When running the backend locally, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These provide interactive API documentation where you can test endpoints directly.
