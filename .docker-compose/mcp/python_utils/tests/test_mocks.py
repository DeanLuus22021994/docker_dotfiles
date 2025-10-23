"""
Test suite to verify mock implementations work correctly.

Tests the API, Database, and Redis mocks to ensure they function
as expected for isolated unit testing.
"""

import pytest


def test_api_mock_fixture(api_mock):
    """Test that API mock fixture provides expected functionality."""
    # Test that api_mock is available
    assert api_mock is not None
    
    # Test mock response retrieval
    response = api_mock.get_mock_response("https://api.github.com/repos/user/docker-examples")
    assert response is not None
    assert response["status_code"] == 200
    assert "name" in response["json"]
    assert response["json"]["name"] == "docker-examples"


def test_api_mock_session_get(api_mock):
    """Test API mock session get method."""
    response = api_mock.mock_session_get("https://api.github.com/repos/user/docker-examples")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "docker-examples"
    assert data["stargazers_count"] == 42


def test_api_mock_unknown_url(api_mock):
    """Test API mock returns 404 for unknown URLs."""
    response = api_mock.mock_session_get("https://unknown.example.com")
    assert response.status_code == 404


def test_database_mock_fixture(database_mock):
    """Test that database mock fixture provides expected functionality."""
    # Test that database_mock is available
    assert database_mock is not None
    
    # Test connection creation
    connection = database_mock.mock_connect()
    assert connection is not None
    
    # Test cursor creation
    cursor = connection.cursor()
    assert cursor is not None


def test_database_mock_query(database_mock):
    """Test database mock query execution."""
    connection = database_mock.mock_connect()
    cursor = connection.cursor()
    
    # Test SELECT query
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    assert len(results) == 2
    assert results[0]["name"] == "Test User"
    assert results[1]["email"] == "admin@example.com"


def test_redis_mock_fixture(redis_mock):
    """Test that Redis mock fixture provides expected functionality."""
    # Test that redis_mock is available
    assert redis_mock is not None


def test_redis_mock_operations(redis_mock):
    """Test Redis mock basic operations."""
    # Test SET and GET
    result = redis_mock.mock.set("test_key", "test_value")
    assert result is True
    
    value = redis_mock.mock.get("test_key")
    assert value == "test_value"
    
    # Test EXISTS
    exists = redis_mock.mock.exists("test_key")
    assert exists == 1
    
    # Test DELETE
    deleted = redis_mock.mock.delete("test_key")
    assert deleted == 1
    
    # Verify key is gone
    value = redis_mock.mock.get("test_key")
    assert value is None


def test_redis_mock_expiration(redis_mock):
    """Test Redis mock expiration functionality."""
    # Set key with expiration
    redis_mock.mock.set("expire_key", "value", ex=3600)
    
    # Check TTL
    ttl = redis_mock.mock.ttl("expire_key")
    assert ttl > 0
    assert ttl <= 3600


def test_redis_mock_keys(redis_mock):
    """Test Redis mock keys operation."""
    # Clear all keys first
    redis_mock.mock.flushall()
    
    # Set some test keys
    redis_mock.mock.set("key1", "value1")
    redis_mock.mock.set("key2", "value2")
    redis_mock.mock.set("key3", "value3")
    
    # Get all keys
    keys = redis_mock.mock.keys("*")
    assert len(keys) == 3
    assert "key1" in keys
    
    # Test pattern matching
    keys = redis_mock.mock.keys("key1")
    assert "key1" in keys


def test_external_services_mocking(mock_external_services):
    """Test that external services are automatically mocked."""
    # This test uses the autouse fixture
    assert mock_external_services is not None
    assert "session" in mock_external_services
    assert "database" in mock_external_services
    assert "redis" in mock_external_services
