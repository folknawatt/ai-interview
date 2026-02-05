"""
Configuration module for loading and exposing environment variables.

This module handles loading configuration from Google Cloud Secret Manager
(if configured) or a local .env file, and provides access to key environment
variables used throughout the application.
"""

import os
import time
from io import StringIO
from dotenv import dotenv_values


def _load_secrets_from_secret_manager():
    """
    Load environment variables from Google Cloud Secret Manager.
    This is called during app startup, not at module import time.
    """
    step_start = time.time()

    project_number = os.getenv('PROJECT_NUMBER')
    secret_id = os.getenv('SECRET_ID')

    if not project_number or not secret_id:
        return

    try:
        # Lazy import - only load when actually needed
        from google.cloud import secretmanager

        client = secretmanager.SecretManagerServiceClient()
        resource_name = f"projects/{project_number}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(
            request={"name": resource_name})
        payload = response.payload.data.decode("UTF-8")

        # Load environment variables from the payload
        env_dict = dotenv_values(stream=StringIO(payload))
        for k, v in env_dict.items():
            os.environ[k] = v
    except Exception as e:
        print(f"[{time.time() - step_start:.3f}s] ❌ Failed to load secrets: {e}")

# =============================================================================
# ENVIRONMENT VARIABLES
# =============================================================================


# Database
DATABASE_URL = os.getenv(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB')}")
