# 🎯 AI Interview Platform

An AI-powered interview platform that combines intelligent question generation with automated candidate evaluation, streamlining the hiring process for HR teams and providing a seamless experience for candidates.

## ✨ Features

### For HR Teams

- 🤖 **AI-Generated Questions**: Automatically generate role-specific interview questions using Google Gemini AI
- 📊 **Role Management**: Create and manage different job roles with customized question sets
- 🎯 **Intelligent Evaluation**: Automated candidate assessment based on responses
- 📈 **Dashboard**: Centralized view of all interviews and candidates

### For Candidates

- 🎤 **Video/Audio Recording**: Record interview responses directly in the browser
- 🔊 **Text-to-Speech**: Questions read aloud using natural-sounding TTS
- 📝 **Transcription**: Automatic speech-to-text conversion using Whisper AI
- ✅ **Instant Feedback**: Get evaluation results immediately after interview completion

## 🏗️ Architecture

### Tech Stack

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

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- FFmpeg installed on your system
- Google Gemini API key

### Backend Setup

#### Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
# Run setup script (Windows PowerShell)
.\scripts\setup.ps1
```

This will:

- Check prerequisites (Python, Node.js, FFmpeg)
- Set up Python virtual environment
- Install all dependencies
- Create storage directories
- Copy `.env.example` to `.env`
- Set up pre-commit hooks

After setup, edit `backend/.env` and add your `GOOGLE_API_KEY`.

#### Option 2: Manual Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd ai-interview
   ```

2. **Set up Python environment**

   ```bash
   cd backend
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   # Using uv (recommended)
   pip install uv
   uv sync --extra dev

   # Or using pip
   pip install -e ".[dev]"
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

5. **Run the backend server**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
   Backend will be available at `http://localhost:8000`

### Frontend Setup

The automated setup script (`.\scripts\setup.ps1`) handles frontend setup too.

**Manual frontend setup:**

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Configure environment**

   ```bash
   cp .env.example .env
   # Set API_BASE_URL=http://localhost:8000
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```
   Frontend will be available at `http://localhost:3000`

### Quick Start (Both Servers)

After running setup, start both servers with one command:

```bash
# Start both backend and frontend
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

Docker support is planned for future releases. See `docs/setup/deployment.md` for manual deployment instructions.

## 📖 Documentation

- [Architecture Overview](docs/architecture/overview.md)
- [API Documentation](docs/api/README.md)
- [Development Guide](docs/guides/contributing.md)
- [Deployment Guide](docs/setup/deployment.md)

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
