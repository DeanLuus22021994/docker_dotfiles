"""
Pytest configuration and fixtures for React Scuba tests.

Provides automatic mocking of external dependencies for isolated testing.
"""

import sys
from pathlib import Path

import pytest

# Add python_utils to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "python_utils"))

# TODO: Create mock files for external dependencies
from api_mock import mock_external_dependencies


@pytest.fixture(autouse=True)
def mock_external_services():
    """
    Automatically mock external API dependencies for all tests.

    This fixture patches HTTP requests, database connections, and Redis
    operations to prevent network calls and external service dependencies
    during unit testing.
    """
    # TODO: Implement external service mocking
    with mock_external_dependencies() as mocks:
        yield mocks


@pytest.fixture
def api_mock():
    """Provide direct access to API mock for specific test scenarios."""
    # TODO: Implement API mock
    from api_mock import api_mock

    return api_mock


@pytest.fixture
def database_mock():
    """Provide direct access to database mock for specific test scenarios."""
    # TODO: Implement database mock
    from database_mock import database_mock

    return database_mock


@pytest.fixture
def redis_mock():
    """Provide direct access to Redis mock for specific test scenarios."""
    # TODO: Implement Redis mock
    from redis_mock import redis_client_mock

    return redis_client_mock
