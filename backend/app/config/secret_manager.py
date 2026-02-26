"""Configuration module for loading and exposing environment variables.

This module handles loading configuration from Google Cloud Secret Manager
(if configured) or a local .env file, and provides access to key environment
variables used throughout the application.
"""

import logging
import os
import time
from io import StringIO

from dotenv import dotenv_values

logger = logging.getLogger(__name__)


def _load_secrets_from_secret_manager():
    """Load secrets from Google Cloud Secret Manager.

    This function is called during application startup to override/augment
    local .env variables with secrets stored in Google Cloud.

    Required environment variables:
    - PROJECT_NUMBER: Google Cloud project number
    - SECRET_ID: Name of the secret containing environment variables

    Security considerations:
    - Service account key should have minimal permissions (secretmanager.secretAccessor)
    - In production (Cloud Run/GKE), use Workload Identity instead of key files
    """
    step_start = time.time()

    # Check if Secret Manager is configured
    project_number = os.getenv("PROJECT_NUMBER")
    secret_id = os.getenv("SECRET_ID")

    if not project_number or not secret_id:
        # Secret Manager not configured - using local .env only
        return

    try:
        # Lazy import - only load Google Cloud SDK when actually needed
        # This avoids import errors in local development without GCP
        from google.cloud import secretmanager

        client = secretmanager.SecretManagerServiceClient()

        # Construct full secret path: projects/{project}/secrets/{secret}/versions/latest
        resource_name = f"projects/{project_number}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": resource_name})
        payload = response.payload.data.decode("UTF-8")

        # Parse .env format from secret payload and inject into os.environ
        # This overrides any local .env values with production secrets
        env_dict = dotenv_values(stream=StringIO(payload))
        for k, v in env_dict.items():
            os.environ[k] = v

        logger.info(f"[{time.time() - step_start:.3f}s] ✅ Secrets loaded from Secret Manager")

    except Exception as e:
        # Log error but don't crash - fall back to local .env
        logger.error(f"[{time.time() - step_start:.3f}s] ❌ Failed to load secrets: {e}")
