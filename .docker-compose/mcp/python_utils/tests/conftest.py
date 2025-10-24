"""
Pytest configuration and fixtures for Docker Compose Utils tests.

Provides automatic mocking of external dependencies for isolated testing.
"""

import sys
from pathlib import Path

import pytest

# Add tests directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent))

from api_mock import mock_external_dependencies


@pytest.fixture(autouse=True)
def mock_external_services():
    """
    Automatically mock external API dependencies for all tests.

    This fixture patches HTTP requests, database connections, and Redis
    operations to prevent network calls and external service dependencies
    during unit testing.
    """
    with mock_external_dependencies() as mocks:
        yield mocks


@pytest.fixture
def api_mock():
    """Provide direct access to API mock for specific test scenarios."""
    from api_mock import api_mock

    return api_mock


@pytest.fixture
def database_mock():
    """Provide direct access to database mock for specific test scenarios."""
    from database_mock import database_mock

    return database_mock


@pytest.fixture
def redis_mock():
    """Provide direct access to Redis mock for specific test scenarios."""
    from redis_mock import redis_client_mock

    return redis_client_mock
