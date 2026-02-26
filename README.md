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
- 📝 **Transcription**: Automatic speech-to-text conversion via Whisper AI.
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

## � Workflow Process

```mermaid
sequenceDiagram
    participant Candidate as 👤 Candidate
    participant Frontend as 🖥️ Frontend (Nuxt/Vue)
    participant Backend as ⚙️ Backend (FastAPI)
    participant AI_Gemini as 🧠 AI (Google Gemini)
    participant AI_Whisper as 🎙️ AI (Whisper/TTS)

    %% 1. Preparation Phase
    rect rgb(240, 248, 255)
        note right of Candidate: 1. Preparation Phase
        Candidate->>Frontend: Upload Resume (PDF)
        Frontend->>Backend: Send resume for analysis
        Backend->>AI_Gemini: Process resume data
        AI_Gemini-->>Backend: Generate personalized questions
        Backend-->>Frontend: Combine with core role questions
    end

    %% 2. Interview Execution Phase
    rect rgb(255, 245, 238)
        note right of Candidate: 2. Interview Execution
        loop For each question
            Backend->>AI_Whisper: Generate text-to-speech audio
            AI_Whisper-->>Frontend: Send audio & question text
            Frontend->>Candidate: Display and read question
            Candidate->>Frontend: Record video response
            Frontend->>Backend: Send video/audio (Real-time)
            Backend->>AI_Whisper: Transcribe audio to text
            AI_Whisper-->>Backend: Transcription complete
            Backend->>AI_Gemini: Evaluate response text
            AI_Gemini-->>Backend: Return score and feedback (Real-time)
        end
    end

    %% 3. Session Completion
    rect rgb(240, 255, 240)
        note right of Candidate: 3. Session Completion
        Backend->>Backend: Aggregate scores
        Backend-->>Frontend: Send final recommendation & feedback
        Frontend-->>Candidate: Display preliminary result & feedback
    end
```

## �📖 Further Documentation

- [Architecture Overview](docs/architecture/overview.md)
- [API Documentation](docs/api/README.md)
- [Docker Deployment Guide](docs/setup/deploy/DOCKER_DEPLOYMENT.md)
- [Contributing Guidelines](CONTRIBUTING.md)
