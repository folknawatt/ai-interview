# syntax=docker/dockerfile:1

#===============================================================================
# Stage 1: Build Stage - Install dependencies with UV
#===============================================================================
FROM python:3.11-slim AS builder

# Copy uv binary from the official image (Best practice)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set build-time environment variables
# UV_LINK_MODE=copy is crucial for multi-stage builds to ensure files 
# are physically copied to the venv, not just hardlinked/symlinked.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=0 \
    VIRTUAL_ENV=/opt/venv

WORKDIR /build

# Install build dependencies
# We still need build-essential/libpq-dev for compiling C extensions if wheels aren't available
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY backend/requirements.txt .

# Create virtual environment and install dependencies using UV
# --mount=type=cache creates a cache for uv to speed up subsequent builds
# We add a build arg to optionally install CPU-only versions of torch/nvidia libs
ARG INSTALL_TYPE=cpu
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv /opt/venv && \
    if [ "$INSTALL_TYPE" = "cpu" ]; then \
    uv pip install --no-cache -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu; \
    else \
    uv pip install --no-cache -r requirements.txt; \
    fi

#===============================================================================
# Stage 2: Runtime Stage - Minimal production image
#===============================================================================
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -d /home/appuser -m appuser

# Set filesystem permissions
RUN mkdir -p /home/appuser && chown -R appuser:appuser /home/appuser

# Install only runtime dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set runtime environment variables
# Note: We include the venv path in PATH so we don't need to activate it explicitly
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app/backend:$PYTHONPATH"

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY backend/ /app/backend/

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000').read()" || exit 1

# Set working directory to backend
WORKDIR /app/backend

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]