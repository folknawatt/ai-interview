# Docker Deployment Guide

Comprehensive instructions for deploying and testing the AI Interview System using Docker.

## 🚀 Quick Start

### 1. Environment Configuration

```bash
cp .env.example .env
nano .env # Ensure the GOOGLE_API_KEY is correctly configured
```

### 2. Build and Run

```bash
DOCKER_BUILDKIT=1 docker-compose build
docker-compose up -d
docker-compose logs -f backend
```

### 3. Accessing Services

- **Backend API:** `http://localhost:8000`
- **Database:** `localhost:5432`

## 📋 Standard Operational Commands

**Development Workflow:**

```bash
# Restart the Backend service
docker-compose restart backend

# Rebuild the Backend service after significant code changes
docker-compose up -d --build backend
```

**Maintenance & Cleanup:**

```bash
docker-compose down # Stop all services
docker-compose down -v # Stop services AND destroy the Database volume (Destructive Action)
```

## 📊 System Monitoring

- **Resource Utilization:** `docker stats`
- **Container Health:** `docker-compose ps`
- **Application Logs:** `docker-compose logs --tail=100 backend`

## 🛡️ Security & Maintenance

- Application containers run as non-root users.
- Automated Health Checks are configured for self-healing.
- **Production Recommendation:** Ensure default database credentials are changed in the `.env` file prior to production deployment.
