# 🎯 AI Interview Platform

An AI-powered interview platform that seamlessly integrates intelligent question generation and automated candidate evaluation, streamlining the hiring process for HR teams and delivering a top-tier candidate experience.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Nuxt 4](https://img.shields.io/badge/Nuxt-4-00DC82.svg)](https://nuxt.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://www.docker.com/)

## ✨ Key Features

**For HR Teams:**

- 🤖 **AI-Generated Questions**: Automatically generate role-specific interview questions using Google Gemini.
- 📊 **Role Management**: Efficiently manage job roles and tailored question sets.
- 🎯 **Intelligent Evaluation**: Automated candidate assessment and scoring.
- 📈 **Dashboard**: Centralized overview of all interviews and candidates.

**For Candidates:**

- 🎤 **Video/Audio Recording**: Record interview responses directly in the browser.
- 🔊 **Text-to-Speech**: Questions are read aloud naturally.
- 📝 **Transcription**: Automatic speech-to-text conversion via Typhoon ASR.
- ✅ **Instant Feedback**: Receive preliminary evaluation results immediately after the interview.

## 🚀 Quick Start

### 🐳 Using Docker (Recommended)

```bash
git clone <repository-url>
cd ai-interview
cp .env.docker.example .env # Ensure you configure your GOOGLE_API_KEY
docker-compose up -d --build
```

Access the system:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### 🛠️ Local Development

**Backend:**

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## Workflow Process

```mermaid
sequenceDiagram
    participant Candidate as 👤 Candidate
    participant Frontend as 🖥️ Frontend (Nuxt)
    participant Backend as ⚙️ Backend (FastAPI)
    participant DB as 🗄️ Database (PostgreSQL)
    participant AI_Gemini as 🧠 AI (Google Gemini)
    participant AI_Vachana as 🗣️ AI (Vachana TTS)
    participant AI_Typhoon as 📝 AI (Typhoon ASR)

    %% 1. Preparation Phase
    rect rgba(0, 150, 255, 0.1)
        note right of Candidate: 1. Preparation Phase
        Candidate->>Frontend: Upload Resume (PDF)
        Frontend->>Backend: POST /interview/upload-pdf
        Backend->>AI_Gemini: Process resume text
        AI_Gemini-->>Backend: Return personalized questions
        Backend->>DB: Save session & questions snapshot
        Backend-->>Frontend: Return session_id & questions
    end

    %% 2. Interview Execution Phase
    rect rgba(255, 150, 0, 0.1)
        note right of Candidate: 2. Interview Execution Phase
        loop For each question
            Frontend->>Backend: GET /interview/session/{id}/question/{index}
            Backend->>DB: Retrieve question snapshot
            Backend->>AI_Vachana: Request TTS audio generation
            AI_Vachana-->>Backend: Return audio file
            Backend-->>Frontend: Return question text & audio_path

            Frontend->>Candidate: Play audio & display question
            Candidate->>Frontend: Record video response
            Frontend->>Backend: POST /interview/upload-answer (video blob)

            Backend->>AI_Typhoon: Extract & transcribe audio to text
            AI_Typhoon-->>Backend: Return transcript

            Backend->>AI_Gemini: Evaluate transcript against role
            AI_Gemini-->>Backend: Return scores & feedback

            Backend->>DB: Save QuestionResult
            Backend-->>Frontend: Return AnalysisResponse
        end
    end

    %% 3. Session Completion
    rect rgba(0, 255, 100, 0.1)
        note right of Candidate: 3. Session Completion Phase
        Frontend->>Backend: POST /interview/complete/{session_id}
        Backend->>DB: Aggregate scores from all questions
        Backend->>DB: Update InterviewSession status
        Backend-->>Frontend: Return final recommendation & scores
        Frontend-->>Candidate: Display Result Page
    end
```

## 📖 Further Documentation

- [Architecture Overview](docs/architecture/overview.md)
- [API Documentation](docs/api/README.md)
- [Docker Deployment Guide](docs/setup/deploy/DOCKER_DEPLOYMENT.md)
- [Contributing Guidelines](CONTRIBUTING.md)
