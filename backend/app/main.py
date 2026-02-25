"""FastAPI backend for AI Interview System."""

from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config.logging_config import configure_logging, get_logger
from app.config.settings import settings
from app.database.db import init_db
from app.exceptions import AppException, convert_exception
from app.routers import auth, hr, interview, reports, tts

# Configure logging immediately
configure_logging(json_format=True)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_application: FastAPI):
    """Application lifespan management - handles startup and shutdown events.

    Startup sequence:
    1. Validate security configuration (warns if using default secrets)
    2. Initialize database (create tables, seed data)
    3. Ready to serve requests

    Shutdown: Cleanup resources if needed
    """
    # ========== Startup ==========
    logger.info("Starting application...")

    # Validate security settings (logs warnings for production unsafe configs)
    settings.validate_security()

    # Initialize database: create tables and seed initial data
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized successfully")

    yield  # Application runs here

    # ========== Shutdown ==========
    # Cleanup resources (connections, temp files, etc.)
    logger.info("Application shutdown")


app = FastAPI(
    title="AI Interview API",
    description=(
        "API for AI-powered interview system with question generation, TTS, and evaluation"
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# Global exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(_request: Request, exc: AppException):
    """Handle custom AppException and return proper JSON response."""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def general_exception_handler(_request: Request, exc: Exception):
    """Handle unexpected exceptions and convert to AppException."""
    app_exc = convert_exception(exc)
    return JSONResponse(status_code=app_exc.status_code, content={"detail": app_exc.detail})


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,  # Required for HttpOnly cookies
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],  # For file downloads
)

# Static File Serving
AUDIO_DIR = Path(settings.tts_audio_dir)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/audio", StaticFiles(directory=str(AUDIO_DIR)), name="audio")

VIDEO_DIR = Path(settings.base_storage_dir) / "videos"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/videos", StaticFiles(directory=str(VIDEO_DIR)), name="videos")

# ============================================================================
# API Routers
# ============================================================================
# Register all API endpoint routers
app.include_router(auth.router)  # Authentication & authorization
app.include_router(hr.router)  # HR management (roles, questions)
app.include_router(interview.router)  # Candidate interview flow
app.include_router(tts.router)  # Text-to-speech generation
app.include_router(reports.router)  # Interview reports & analytics


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint to verify API is running."""
    return {"message": "AI Interview API is running properly."}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.server_host, port=settings.server_port, reload=True)
