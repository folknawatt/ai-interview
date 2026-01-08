- include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
  1: # 🎯 AI Interview Platform
  2:
  3: [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  4: [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
  5: [![Nuxt 3](https://img.shields.io/badge/Nuxt-3-00DC82.svg)](https://nuxt.com)
  6: [![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg)](https://fastapi.tiangolo.com)
  7: [![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://www.docker.com/)
  8:
  9: An AI-powered interview platform that combines intelligent question generation with automated candidate evaluation, streamlining the hiring process for HR teams and providing a seamless experience for candidates.
  10:
  11: ## ✨ Features
  12:
  13: ### For HR Teams
  14:
  15: - 🤖 **AI-Generated Questions**: Automatically generate role-specific interview questions using Google Gemini AI
  16: - 📊 **Role Management**: Create and manage different job roles with customized question sets
  17: - 🎯 **Intelligent Evaluation**: Automated candidate assessment based on responses
  18: - 📈 **Dashboard**: Centralized view of all interviews and candidates
  19:
  20: ### For Candidates
  21:
  22: - 🎤 **Video/Audio Recording**: Record interview responses directly in the browser
  23: - 🔊 **Text-to-Speech**: Questions read aloud using natural-sounding TTS
  24: - 📝 **Transcription**: Automatic speech-to-text conversion using Whisper AI
  25: - ✅ **Instant Feedback**: Get evaluation results immediately after interview completion
  26:
  27: ## 🏗️ Architecture
  28:
  29: ### System Overview
  30:
  31: `mermaid
32: graph TD
33:     subgraph "Client Layer"
34:         Candidate[Candidate Interface]
35:         HR[HR Dashboard]
36:     end
37:
38:     subgraph "Application Layer"
39:         Nuxt[Frontend (Nuxt 3)]
40:         FastAPI[Backend (FastAPI)]
41:     end
42:
43:     subgraph "Data & AI Layer"
44:         DB[(PostgreSQL)]
45:         Gemini[Google Gemini AI]
46:         Whisper[Whisper ASR]
47:         TTS[Edge TTS]
48:     end
49:
50:     Candidate & HR -->|HTTPS| Nuxt
51:     Nuxt -->|REST API| FastAPI
52:     FastAPI -->|SQL| DB
53:     FastAPI -->|GenAI| Gemini
54:     FastAPI -->|Transcribe| Whisper
55:     FastAPI -->|Speech| TTS
56: `
  57:
  58: ### User Flow
  59:
  60: `mermaid
61: sequenceDiagram
62:     participant U as User
63:     participant F as Frontend
64:     participant B as Backend
65:     participant A as AI Services
66:
67:     U->>F: Request Interview/Role
68:     F->>B: API Call
69:     B->>A: Generate/Process
70:     A-->>B: AI Result
71:     B-->>F: JSON Response
72:     F-->>U: Render UI
73: `
  74:
  75: ### Tech Stack

**Backend:**

- FastAPI (Python 3.11+)
- Google Gemini AI (Question Generation & Evaluation)
- Whisper AI (Speech-to-Text)
- Pydantic Settings (Configuration Management)
- Edge TTS / Google TTS (Text-to-Speech)

**Frontend:**

- Nuxt 3 (Vue 3 Framework)
- TypeScript
- Tailwind CSS
- Pinia (State Management)
- VueUse (Composables)

**Key Libraries:**

- FFmpeg (Audio/Video Processing)
- MoviePy (Video Manipulation)
- faster-whisper (Optimized Transcription)

## 🚀 Quick Start

### 🐳 Using Docker (Production & Dev)

The easiest way to get started is using Docker.

```bash
# 1. Clone the repository
git clone <repository-url>
cd ai-interview

# 2. Setup environment
cp .env.docker.example .env
# Edit .env and add your GOOGLE_API_KEY

# 3. Start services
docker-compose up -d --build
```

Visit:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Documentation: `http://localhost:8000/docs`

### 🛠️ Local Development

For developers who want to run services individually.

#### Prerequisites

- Python 3.11+
- Node.js 18+
- FFmpeg

#### Automated Setup (Windows)

```powershell
# Setup everything
.\scripts\setup.ps1

# Run dev servers
.\scripts\dev.ps1
```

## 📁 Project Structure

```
ai-interview/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── core/          # Business logic (AI, audio, TTS)
│   │   ├── routers/       # API endpoints
│   │   ├── models.py      # Pydantic models
│   │   └── main.py        # FastAPI app
│   ├── config/            # Configuration
│   └── tests/             # Backend tests
│
├── frontend/              # Nuxt 3 frontend
│   ├── components/        # Vue components
│   ├── composables/       # Composable functions
│   ├── pages/             # Route pages
│   ├── store/             # Pinia stores
│   └── types/             # TypeScript types
│
└── tests/                 # Integration tests
```

## 🔧 Configuration

### Backend Environment Variables

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Frontend Environment Variables

```env
API_BASE_URL=http://localhost:8000
```

## 🔒 Security

We take security seriously. Please review our security implementation:

- **Authentication**: Usage of API Keys for external services (Gemini).
- **Data Protection**:
  - No sensitive data committed to repo (enforced by `.gitignore` & hooks).
  - Environment variables for secrets.
  - Temporary storage cleanup for audio/video files.
- **Compliance**:
  - GDPR/PDPA: Candidate data is processed ephemerally or stored with consent.

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## 📡 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

**HR Routes** (`/hr`)

- `POST /hr/generate-questions` - Generate interview questions for a role
- `GET /hr/roles` - List all roles
- `POST /hr/roles` - Create new role

**Interview Routes** (`/interview`)

- `POST /interview/upload-video` - Upload candidate video response
- `POST /interview/evaluate` - Evaluate candidate responses
- `GET /interview/result/{id}` - Get evaluation results

**TTS Routes** (`/tts`)

- `POST /tts/generate` - Generate speech from text

## 🛠️ Development

### Development Workflow

**PowerShell Scripts:**

```bash
# Setup project
.\scripts\setup.ps1

# Start dev servers
.\scripts\dev.ps1

# Clean caches
.\scripts\clean.ps1
```

### Code Quality Tools

**Backend:**

```bash
# Format code
black .

# Lint
ruff check .

# Type checking
mypy app/
```

**Frontend:**

```bash
# Lint
npm run lint

# Format
npm run format

# Type check
npm run type-check
```

### Running with Docker

Docker support is planned for future releases. See [docs/setup/deploy/DOCKER_DEPLOYMENT.md](docs/setup/deploy/DOCKER_DEPLOYMENT.md) for manual deployment instructions.

## 📖 Documentation

- [Architecture Overview](docs/architecture/overview.md)
- [API Documentation](docs/api/README.md)
- [Development Guide](CONTRIBUTING.md)
- [Deployment Guide](docs/setup/deploy/DOCKER_DEPLOYMENT.md)

## 🤝 Contributing

We welcome contributions!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

[Your License Here]

## 🙏 Acknowledgments

- Google Gemini AI for question generation and evaluation
- OpenAI Whisper for speech recognition
- FastAPI and Nuxt.js communities

## 📧 Contact

For questions or support, please contact [your-email@example.com]

---

**Made with ❤️ for better hiring experiences**
