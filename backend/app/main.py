"""
FastAPI backend for AI Interview System.
"""
import logging
import uvicorn
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.settings import settings
from app.exceptions import AppException, convert_exception
from app.database.db import init_db
from app.routers import hr, interview, reports, tts

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_application: FastAPI):
    """Application lifespan management - startup and shutdown."""
    # Startup
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")
    yield
    # Shutdown (cleanup if needed)
    logger.info("Application shutdown")


app = FastAPI(
    title="AI Interview API",
    description=(
        "API for AI-powered interview system with question generation, "
        "TTS, and evaluation"
    ),
    version="1.0.0",
    lifespan=lifespan
)


# Global exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(_request: Request, exc: AppException):
    """Handle custom AppException and return proper JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(_request: Request, exc: Exception):
    """Handle unexpected exceptions and convert to AppException."""
    app_exc = convert_exception(exc)
    return JSONResponse(
        status_code=app_exc.status_code,
        content={"detail": app_exc.detail}
    )


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hr.router)
app.include_router(interview.router)
app.include_router(tts.router)
app.include_router(reports.router)


@app.get("/")
def root() -> Dict[str, str]:
    """Root endpoint to verify API is running."""
    return {"message": "AI Interview API is running properly."}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )
