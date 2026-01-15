#===============================================================================
# Stage 1: Builder - เน้นความเร็วในการติดตั้งและ Caching
#===============================================================================
FROM python:3.11-slim AS builder

# Copy UV binary (Reusing official image is faster/safer)
COPY --from=ghcr.io/astral-sh/uv:0.5.14 /uv /bin/uv

# Environment Variables for Build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=0 \
    VIRTUAL_ENV=/opt/venv

WORKDIR /build

# Install system dependencies (Git is often needed for installing deps from source)
# Use standard Debian mirrors for reliability
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker Layer Caching
COPY pyproject.toml uv.lock ./

# Install Python Dependencies via UV
RUN uv venv /opt/venv && \
    uv sync --frozen
#===============================================================================
# Stage 2: Runtime - เน้นขนาดเล็กและความปลอดภัย
#===============================================================================
FROM python:3.11-slim

# Create a non-root user (Security Best Practice)
RUN groupadd -r appuser && useradd -r -g appuser -d /home/appuser -m appuser

# Set Runtime ENV
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app/backend:$PYTHONPATH"

WORKDIR /app



# Install Runtime Libraries
# Clean up apt lists in the same layer to save space
# ติดตั้ง Runtime Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# COPY --chown is atomic (Doesn't double the layer size)
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv
COPY --chown=appuser:appuser backend/ /app/backend/

# Switch context to non-root
USER appuser

# Port & Healthcheck
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000').read()" || exit 1

WORKDIR /app/backend

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]