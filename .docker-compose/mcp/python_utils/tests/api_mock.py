"""
Mock services for external API dependencies in tests.

Provides mock HTTP responses and database connections to enable
fast, isolated unit testing without external service dependencies.
"""

import json
from typing import Any, Dict, Optional
from unittest.mock import Mock

from database_mock import database_mock
from redis_mock import redis_client_mock


class APIMock:
    """
    Mock external API responses for testing.

    Provides predefined responses for common external services
    to avoid network calls during unit tests.
    """

    def __init__(self):
        self.mock_responses = {
            "https://api.github.com/repos/deanluus22021994/react-scuba": {
                "status_code": 200,
                "json": {
                    "name": "react-scuba",
                    "full_name": "deanluus22021994/react-scuba",
                    "description": "React Scuba diving application",
                    "html_url": "https://github.com/deanluus22021994/react-scuba",
                    "stargazers_count": 42,
                    "forks_count": 7,
                },
            },
            "https://docs.docker.com/compose/": {
                "status_code": 200,
                "json": {"title": "Docker Compose Documentation"},
            },
            "https://fastapi.tiangolo.com/tutorial/": {
                "status_code": 200,
                "json": {"title": "FastAPI Tutorial"},
            },
            "https://www.python.org/": {
                "status_code": 200,
                "json": {"title": "Python Programming Language"},
            },
        }

    def get_mock_response(self, url: str) -> dict[str, Any] | None:
        """Get mock response for a URL."""
        return self.mock_responses.get(url)

    def mock_session_get(self, url: str, **kwargs):
        """Mock requests session get method."""
        mock_response = self.get_mock_response(url)
        if mock_response:
            response_mock = Mock()
            response_mock.status_code = mock_response["status_code"]
            response_mock.json.return_value = mock_response["json"]
            response_mock.text = json.dumps(mock_response["json"])
            return response_mock
        else:
            # Return 404 for unknown URLs
            response_mock = Mock()
            response_mock.status_code = 404
            response_mock.raise_for_status.side_effect = Exception("404 Client Error")
            return response_mock

    def mock_session_head(self, url: str, **kwargs):
        """Mock requests session head method."""
        mock_response = self.get_mock_response(url)
        if mock_response:
            response_mock = Mock()
            response_mock.status_code = mock_response["status_code"]
            return response_mock
        else:
            response_mock = Mock()
            response_mock.status_code = 404
            return response_mock


# Global mock instances
api_mock = APIMock()


def mock_external_dependencies():
    """
    Context manager to mock all external dependencies.

    Patches requests, database connections, and Redis operations
    for isolated unit testing.
    """
    from contextlib import contextmanager

    @contextmanager
    def _mock_context():
        from unittest.mock import patch

        # Mock requests session
        session_mock = Mock()
        session_mock.get.side_effect = api_mock.mock_session_get
        session_mock.head.side_effect = api_mock.mock_session_head

        # Mock database connections
        db_mock = Mock()
        db_mock.connect.side_effect = database_mock.mock_connect

        # Mock Redis
        redis_client_mock_instance = Mock()
        redis_client_mock_instance.get.side_effect = redis_client_mock.get
        redis_client_mock_instance.set.side_effect = redis_client_mock.set
        redis_client_mock_instance.delete.side_effect = redis_client_mock.delete
        redis_client_mock_instance.exists.side_effect = redis_client_mock.exists

        with (
            patch.multiple(
                "react_scuba_utils.config.settings.HTTPConfig", session=session_mock
            ),
            patch.multiple("psycopg2", connect=database_mock.mock_connect),
            patch.multiple("redis", Redis=lambda **kwargs: redis_client_mock_instance),
        ):
            yield {
                "session": session_mock,
                "database": db_mock,
                "redis": redis_client_mock_instance,
            }

    return _mock_context()


def setup_test_mocks():
    """
    Setup function for test files to enable mocking.

    Call this in test setup to mock external dependencies.
    """
    return mock_external_dependencies()
