# Contributing to AI Interview Platform

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to **AI Interview Platform**. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## 🛠️ Development Setup

1. **Clone the repo**

   ```bash
   git clone <repository_url>
   cd ai-interview
   ```

2. **Run Setup Script (Windows)**

   ```powershell
   .\scripts\setup.ps1
   ```

   This will install Python dependencies (`uv`), Node.js dependencies (`npm`), and setup pre-commit hooks.

3. **Start Development**
   ```powershell
   .\scripts\dev.ps1
   ```

## 🧪 Testing

Before submitting a Pull Request, please ensure all tests pass.

- **Backend**:

  ```bash
  cd backend
  uv run pytest
  ```

- **Frontend**:
  ```bash
  cd frontend
  npm run test
  ```

## 📝 Code Style

We enforce code style using `pre-commit` hooks.

- **Python**: `black`, `ruff`, `mypy`
- **Frontend**: `eslint`, `prettier`

If you commit and the hooks fail, the commit will be blocked. Fix the issues (or let the tools auto-fix them) and commit again.

## 🔀 Pull Request Process

1. Create a branch from `main` (`git checkout -b feature/amazing-feature`).
2. Implement your changes.
3. Add tests if applicable.
4. Ensure all tests and linting checks pass.
5. Create a Pull Request against `main`.
6. Describe your changes detailedly.

## 🐛 Bug Reports

Open an issue and include:

- A clear title and description.
- Steps to reproduce the error.
- Environment details (OS, Browser, etc.).
