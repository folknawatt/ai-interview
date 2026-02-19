# Changelog

All notable changes to the AI Interview Platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Project structure improvements
- `.editorconfig` for consistent code formatting
- `.node-version` for Node.js version management
- LICENSE file (MIT)
- Comprehensive project structure review documentation

### Changed

- Standardized dependency management to use only `pyproject.toml` (removed `requirements.txt`)
- Standardized frontend package manager to npm (removed `pnpm-lock.yaml`)
- Fixed `.gitignore` overly broad 'tests' pattern
- Refactored database repositories to use BaseRepository pattern
- Updated dependencies (uv.lock)

### Removed

- Duplicate `requirements.txt` file
- Duplicate `pnpm-lock.yaml` file
- Duplicate `backend/questions_db.json` configuration file

## [0.1.0] - 2025-12-08

### Added

- Initial project structure with backend (FastAPI) and frontend (Nuxt 4)
- AI-powered question generation using Google Gemini
- Automated candidate evaluation
- Video/audio recording and transcription using Whisper AI
- Text-to-speech for questions using Edge TTS
- HR dashboard for role and question management
- Candidate interview flow (login, questions, recording, results)
- Code quality tools (Black, Ruff, MyPy, ESLint, Prettier)
- Pre-commit hooks configuration
- Test framework setup (pytest, Vitest)
- Comprehensive README and CONTRIBUTING documentation
- Architecture and API documentation structure

### Backend Features

- FastAPI REST API with automatic OpenAPI documentation
- Google Gemini integration for question generation and evaluation
- Whisper AI integration for speech-to-text transcription
- Edge TTS/Google TTS integration for text-to-speech
- Audio/video processing with FFmpeg and MoviePy
- Pydantic models for request/response validation
- Centralized configuration management
- Structured logging

### Frontend Features

- Nuxt 4 with TypeScript
- Vue 3 Composition API
- Pinia state management
- Tailwind CSS styling
- HR routes (dashboard, question generator, role management)
- Candidate routes (login, questions, recording, results)
- API service layer with composables
- Type-safe TypeScript interfaces

### Development Tools

- Python 3.11+ with uv package manager
- Node.js 18+ with npm
- Black code formatter (line length: 100)
- Ruff linter with comprehensive rules
- MyPy type checker
- ESLint + Prettier for frontend
- pytest with coverage reporting
- Vitest for frontend testing
- Pre-commit hooks for automated quality checks

---

## Version History

- **0.1.0** - Initial release with core features
- **Unreleased** - Ongoing development and improvements

---

## Legend

- `Added` - New features
- `Changed` - Changes in existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security-related changes
