# Architecture Overview

## 🏗️ High-Level Architecture

The AI Interview Platform is designed as a Decoupled Full-Stack Application, maintaining a strict separation of concerns between the Frontend and Backend layers.

```mermaid
graph TB
    subgraph "Frontend - Nuxt 4"
        UI[Vue Components]
        Store[Pinia Store]
        Composables[Composables]
        UI --> Composables
        Composables --> Store
    end

    subgraph "Backend - FastAPI"
        API[API Routes]
        Services[Business Logic]
        Core[Core Modules]
        API --> Services
        Services --> Core
    end

    subgraph "External Services"
        Gemini[Google Gemini AI]
        Typhoon[Typhoon ASR]
        TTS[Vachana TTS]
    end

    subgraph "Storage"
        Database[(Database)]
    end

    Composables -->|HTTP/REST| API
    Core --> Gemini
    Core --> Typhoon
    Core --> TTS
    Services --> Database
```

## 🧩 Component Overview

### Frontend (Nuxt 4)

- **Framework:** Nuxt 4 (Vue 3, leveraging SSR Capabilities)
- **State Management:** Pinia
- **Styling:** Tailwind CSS
- **Type Safety:** TypeScript

### Backend (FastAPI)

- **Framework:** FastAPI (Python 3.11+)
- **AI Engine:** Google Gemini AI (Question Generation & Evaluation)
- **Speech Recognition:** Typhoon ASR
- **Text-to-Speech:** Vachana TTS

## 🔄 Data Flow

**Interview Lifecycle:**

1. **Preparation:** The candidate uploads their Resume (PDF). The AI analyzes the document to construct personalized questions integrated with the core role questions.
2. **Interview Execution:**
   - Questions are presented on-screen accompanied by text-to-speech audio.
   - The candidate records a video response.
   - The video is transmitted to the Backend, where the audio is extracted, transcribed via Typhoon ASR, and evaluated in real-time by Google Gemini.
3. **Session Completion:** The system aggregates the individual question scores to yield a final recommendation and holistic feedback.

### Workflow Process Diagram

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

## 🔒 Security Best Practices

- Strict API Key management via Environment Variables.
- RESTful endpoints secured by configurable CORS Origins.
- Secure file upload handling with automated temporary file cleanup.

## 📈 Scalability Considerations

- Docker-ready architecture enabling horizontal scaling.
- Pluggable components facilitating future migration of storage to Cloud Storage (S3/GCS) and caching mechanisms to Redis.
