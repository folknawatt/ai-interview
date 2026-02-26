# Contributing to AI Interview Platform

First off, thank you for considering contributing to the **AI Interview Platform**!

## 🛠️ Development Setup

1. **Clone the repository**

   ```bash
   git clone <repository_url>
   cd ai-interview
   ```

2. **Backend Setup**

   ```bash
   cd backend
   uv sync
   uv run uvicorn app.main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 🧪 Testing

Please ensure all tests pass before submitting a Pull Request:

- **Backend**: (Tests coming soon)
- **Frontend**: `cd frontend && npm run test`

## 📝 Code Style

We enforce code style using `pre-commit` hooks:

- **Python**: `black`, `ruff`, `mypy`
- **Frontend**: `eslint`, `prettier`

## 🔀 Pull Request Process

1. Create a new branch from `main` (e.g., `feature/amazing-feature`).
2. Implement your changes and add necessary tests.
3. Ensure all CI/Linting checks pass.
4. Submit a Pull Request to `main` with a clear description of the changes.

## 🐛 Bug Reports

If you find a bug, please open an Issue with a clear title, reproduction steps, and environment details (OS, Browser, etc.).
