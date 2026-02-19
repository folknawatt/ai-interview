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

### Upload Video

Upload candidate's video/audio response.

**Endpoint:** `POST /interview/upload-video`

**Content-Type:** `multipart/form-data`

**Form Data:**

```
video: (binary file data)
question_id: "q1"
candidate_id: "cand123"
```

**Response:** `200 OK`

```json
{
  "upload_id": "upload123",
  "transcription": "My answer to the question...",
  "duration": 120.5,
  "status": "completed"
}
```

### Evaluate Interview

Evaluate all candidate responses.

**Endpoint:** `POST /interview/evaluate`

**Request Body:**

```json
{
  "candidate_id": "cand123",
  "responses": [
    {
      "question_id": "q1",
      "transcript": "My answer to question 1...",
      "upload_id": "upload123"
    }
  ]
}
```

**Response:** `200 OK`

```json
{
  "evaluation_id": "eval456",
  "candidate_id": "cand123",
  "overall_score": 85,
  "feedback": "Strong technical knowledge...",
  "question_scores": [
    {
      "question_id": "q1",
      "score": 90,
      "feedback": "Excellent system design approach"
    }
  ],
  "evaluated_at": "2025-12-09T01:00:00Z"
}
```

### Get Result

Get evaluation results for a candidate.

**Endpoint:** `GET /interview/result/{evaluation_id}`

**Response:** `200 OK`

```json
{
  "evaluation_id": "eval456",
  "overall_score": 85,
  "feedback": "Strong candidate...",
  "question_scores": [...]
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
