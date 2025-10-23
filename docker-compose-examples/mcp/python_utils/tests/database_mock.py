"""
Mock database connections for testing.

Provides in-memory database simulation for PostgreSQL operations
to enable fast, isolated unit testing.
"""

from typing import Any, Dict, List, Optional
from unittest.mock import Mock


class DatabaseMock:
    """
    Mock database connections for testing.

    Provides in-memory database simulation for PostgreSQL operations.
    """

    def __init__(self):
        self.connections = {}
        self.data = {
            "users": [
                {"id": 1, "name": "Test User", "email": "test@example.com"},
                {"id": 2, "name": "Admin User", "email": "admin@example.com"}
            ],
            "courses": [
                {"id": 1, "title": "Open Water Diver", "level": "beginner"},
                {"id": 2, "title": "Advanced Open Water", "level": "intermediate"}
            ],
            "dive_sites": [
                {"id": 1, "name": "Great Barrier Reef", "location": "Australia"},
                {"id": 2, "name": "Maui", "location": "Hawaii"}
            ]
        }

    def mock_connect(self, **kwargs):
        """Mock database connection."""
        connection_mock = Mock()
        connection_mock.cursor.return_value = self.mock_cursor()
        connection_mock.close = Mock()
        return connection_mock

    def mock_cursor(self):
        """Mock database cursor with query simulation."""
        cursor_mock = Mock()

        def mock_execute(query: str, params: tuple | None = None):
            """Simulate SQL execution."""
            if "SELECT" in query.upper():
                if "users" in query.lower():
                    cursor_mock.fetchall.return_value = self.data["users"]
                elif "courses" in query.lower():
                    cursor_mock.fetchall.return_value = self.data["courses"]
                elif "dive_sites" in query.lower():
                    cursor_mock.fetchall.return_value = self.data["dive_sites"]
                else:
                    cursor_mock.fetchall.return_value = []
            elif "INSERT" in query.upper():
                # Simulate insert success
                pass
            elif "UPDATE" in query.upper():
                # Simulate update success
                pass
            elif "DELETE" in query.upper():
                # Simulate delete success
                pass

        cursor_mock.execute = mock_execute
        cursor_mock.fetchall = Mock(return_value=[])
        cursor_mock.fetchone = Mock(return_value=None)
        cursor_mock.close = Mock()
        return cursor_mock


# Global instance
database_mock = DatabaseMock()
