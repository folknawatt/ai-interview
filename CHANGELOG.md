# Changelog

All notable changes to the AI Interview Platform will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Project structure improvements.
- `.editorconfig`, `.node-version`, and LICENSE (MIT).
- Comprehensive project structure documentation.

### Changed

- Standardized dependency management using `pyproject.toml` (Backend) and `npm` (Frontend).
- Improved `.gitignore` configurations.
- Refactored Database Repositories to use the BaseRepository pattern.

### Removed

- Redundant files: `requirements.txt`, `pnpm-lock.yaml`, `backend/questions_db.json`.

## [0.1.0] - 2025-12-08

### Added

- Initial project structure with FastAPI (Backend) and Nuxt 4 (Frontend).
- AI-powered question generation and automated candidate evaluation via Google Gemini.
- Video/audio recording and speech-to-text transcription via Whisper AI.
- Text-to-speech (TTS) integration for question dictation.
- HR Dashboard for role and question management.
- Code quality and formatting tools (Black, Ruff, ESLint, Prettier, etc.).
