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
    participant Frontend as 🖥️ Frontend (Nuxt/Vue)
    participant Backend as ⚙️ Backend (FastAPI)
    participant AI_Gemini as 🧠 AI (Google Gemini)
    participant AI_Audio as 🎙️ Audio Services (Typhoon/TTS)

    %% 1. Preparation Phase
    rect rgba(0, 150, 255, 0.1)
        note right of Candidate: 1. Preparation Phase
        Candidate->>Frontend: Upload Resume (PDF)
        Frontend->>Backend: Send resume for analysis
        Backend->>AI_Gemini: Process resume data
        AI_Gemini-->>Backend: Generate personalized questions
        Backend-->>Frontend: Combine with core role questions
    end

    %% 2. Interview Execution Phase
    rect rgba(255, 150, 0, 0.1)
        note right of Candidate: 2. Interview Execution
        loop For each question
            Backend->>AI_Audio: Generate text-to-speech audio
            AI_Audio-->>Frontend: Send audio & question text
            Frontend->>Candidate: Display and read question
            Candidate->>Frontend: Record video response
            Frontend->>Backend: Send video/audio (Real-time)
            Backend->>AI_Audio: Transcribe audio to text
            AI_Audio-->>Backend: Transcription complete
            Backend->>AI_Gemini: Evaluate response text
            AI_Gemini-->>Backend: Return score and feedback (Real-time)
        end
    end

    %% 3. Session Completion
    rect rgba(0, 255, 100, 0.1)
        note right of Candidate: 3. Session Completion
        Backend->>Backend: Aggregate scores
        Backend-->>Frontend: Send final recommendation & feedback
        Frontend-->>Candidate: Display preliminary result & feedback
    end
```

## 🔒 Security Best Practices

- Strict API Key management via Environment Variables.
- RESTful endpoints secured by configurable CORS Origins.
- Secure file upload handling with automated temporary file cleanup.

## 📈 Scalability Considerations

- Docker-ready architecture enabling horizontal scaling.
- Pluggable components facilitating future migration of storage to Cloud Storage (S3/GCS) and caching mechanisms to Redis.
