"""
Unit tests for FastAPI endpoints.

Comprehensive test coverage for API endpoints, middleware, and error handling.
"""

from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from docker_examples_utils.api import app
from docker_examples_utils.services.component_inventory import ComponentInventoryService
from docker_examples_utils.services.link_checker import LinkCheckerService


class TestAPIEndpoints:
    """Test suite for FastAPI endpoints."""

    @pytest.fixture
    def client(self) -> TestClient:
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def mock_inventory_service(self) -> Mock:
        """Mock ComponentInventoryService."""
        mock_service = Mock(spec=ComponentInventoryService)
        mock_service.generate_inventory.return_value = {
            "components": [
                {
                    "name": "Button",
                    "category": "components",
                    "file_path": "/src/Button.jsx",
                    "exports": ["Button", "ButtonVariant"],
                    "imports": ["react"],
                    "size_bytes": 1024
                }
            ],
            "pages": [],
            "hooks": [],
            "utils": []
        }
        return mock_service

    @pytest.fixture
    def mock_link_checker_service(self) -> Mock:
        """Mock LinkCheckerService."""
        mock_service = Mock(spec=LinkCheckerService)
        mock_service.check_links_concurrent.return_value = {
            "valid": ["https://example.com"],
            "broken": [],
            "skipped": ["http://localhost:3000"]
        }
        return mock_service

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns API information."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "version" in data
        assert "python_version" in data
        assert "free_threaded" in data
        assert "interpreters" in data
        assert "endpoints" in data

        # Check that endpoints are documented
        endpoints = data["endpoints"]
        assert "/inventory" in endpoints
        assert "/health" in endpoints
        assert "/links/check" in endpoints

    def test_health_endpoint(self, client: TestClient):
        """Test health endpoint returns system status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert "timestamp" in data
        assert "python_version" in data
        assert "features" in data

    @patch('docker_examples_utils.api.ComponentInventoryService')
    def test_inventory_endpoint_success(self, mock_service_class: Mock, client: TestClient, mock_inventory_service: Mock):
        """Test inventory endpoint with successful component analysis."""
        mock_service_class.return_value = mock_inventory_service

        response = client.get("/inventory")

        assert response.status_code == 200
        data = response.json()

        # Check that categories exist
        assert "components" in data
        assert "pages" in data
        assert "hooks" in data
        assert "utils" in data

        # Check component data structure
        components = data["components"]
        assert len(components) == 1
        component = components[0]
        assert component["name"] == "Button"
        assert component["category"] == "components"
        assert "exports" in component
        assert "imports" in component
        assert "size_bytes" in component

    @patch('docker_examples_utils.api.ComponentInventoryService')
    def test_inventory_endpoint_with_src_path(self, mock_service_class: Mock, client: TestClient, mock_inventory_service: Mock):
        """Test inventory endpoint with custom src_path parameter."""
        mock_service_class.return_value = mock_inventory_service

        response = client.get("/inventory?src_path=custom/src")

        assert response.status_code == 200
        # Verify the service was created with the custom path
        mock_service_class.assert_called_once()
        call_args = mock_service_class.call_args
        assert call_args[1]["config"].src_path == "custom/src"

    @patch('docker_examples_utils.api.ComponentInventoryService')
    def test_inventory_endpoint_service_error(self, mock_service_class: Mock, client: TestClient):
        """Test inventory endpoint handles service errors gracefully."""
        # Mock service to raise an exception
        mock_service = Mock()
        mock_service.generate_inventory.side_effect = Exception("Analysis failed")
        mock_service_class.return_value = mock_service

        response = client.get("/inventory")

        assert response.status_code == 500
        data = response.json()
        assert "detail" in data

    @patch('docker_examples_utils.api.LinkCheckerService')
    def test_links_check_endpoint_success(self, mock_service_class: Mock, client: TestClient, mock_link_checker_service: Mock):
        """Test links check endpoint with successful validation."""
        mock_service_class.return_value = mock_link_checker_service

        response = client.get("/links/check")

        assert response.status_code == 200
        data = response.json()

        assert "valid" in data
        assert "broken" in data
        assert "skipped" in data
        assert data["valid"] == ["https://example.com"]
        assert data["broken"] == []
        assert data["skipped"] == ["http://localhost:3000"]

    @patch('docker_examples_utils.api.LinkCheckerService')
    def test_links_check_endpoint_with_parameters(self, mock_service_class: Mock, client: TestClient, mock_link_checker_service: Mock):
        """Test links check endpoint with custom parameters."""
        mock_service_class.return_value = mock_link_checker_service

        response = client.get("/links/check?workers=5&timeout=30")

        assert response.status_code == 200
        # Verify service was created with custom parameters
        mock_service_class.assert_called_once()
        call_args = mock_service_class.call_args
        config = call_args[0][0]  # First positional argument is config
        assert config.max_workers == 5
        assert config.timeout == 30

    @patch('docker_examples_utils.api.LinkCheckerService')
    def test_links_check_endpoint_service_error(self, mock_service_class: Mock, client: TestClient):
        """Test links check endpoint handles service errors gracefully."""
        mock_service = Mock()
        mock_service.check_links_concurrent.side_effect = Exception("Link checking failed")
        mock_service_class.return_value = mock_service

        response = client.get("/links/check")

        assert response.status_code == 500
        data = response.json()
        assert "detail" in data

    def test_correlation_id_middleware(self, client: TestClient):
        """Test correlation ID middleware adds correlation ID to responses."""
        response = client.get("/")

        assert response.status_code == 200
        # Check that correlation ID header is present
        assert "X-Correlation-ID" in response.headers
        correlation_id = response.headers["X-Correlation-ID"]
        assert len(correlation_id) > 0  # Should be a valid UUID

    def test_correlation_id_passthrough(self, client: TestClient):
        """Test correlation ID is passed through from request headers."""
        test_correlation_id = "test-correlation-123"
        response = client.get("/", headers={"X-Correlation-ID": test_correlation_id})

        assert response.status_code == 200
        assert response.headers["X-Correlation-ID"] == test_correlation_id

    @patch('docker_examples_utils.api.logging')
    def test_error_handling_middleware(self, mock_logging: Mock, client: TestClient):
        """Test error handling middleware catches and logs exceptions."""
        # Force an error by patching a service to raise an exception
        with patch('docker_examples_utils.api.ComponentInventoryService') as mock_service_class:
            mock_service = Mock()
            mock_service.generate_inventory.side_effect = ValueError("Test error")
            mock_service_class.return_value = mock_service

            response = client.get("/inventory")

            assert response.status_code == 500
            # Verify error was logged
            mock_logging.getLogger.return_value.error.assert_called()

    def test_invalid_endpoint(self, client: TestClient):
        """Test accessing invalid endpoint returns 404."""
        response = client.get("/nonexistent")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_method_not_allowed(self, client: TestClient):
        """Test using wrong HTTP method returns 405."""
        response = client.post("/")

        assert response.status_code == 405
        data = response.json()
        assert "detail" in data

    @patch('docker_examples_utils.api.ComponentInventoryService')
    def test_inventory_endpoint_empty_results(self, mock_service_class: Mock, client: TestClient):
        """Test inventory endpoint with empty results."""
        mock_service = Mock()
        mock_service.generate_inventory.return_value = {
            "components": [],
            "pages": [],
            "hooks": [],
            "utils": []
        }
        mock_service_class.return_value = mock_service

        response = client.get("/inventory")

        assert response.status_code == 200
        data = response.json()

        # All categories should be present but empty
        assert data["components"] == []
        assert data["pages"] == []
        assert data["hooks"] == []
        assert data["utils"] == []

    @patch('docker_examples_utils.api.LinkCheckerService')
    def test_links_check_endpoint_empty_docs(self, mock_service_class: Mock, client: TestClient):
        """Test links check endpoint when no markdown files exist."""
        mock_service = Mock()
        mock_service.check_links_concurrent.return_value = {
            "valid": [],
            "broken": [],
            "skipped": []
        }
        mock_service_class.return_value = mock_service

        response = client.get("/links/check")

        assert response.status_code == 200
        data = response.json()
        assert data["valid"] == []
        assert data["broken"] == []
        assert data["skipped"] == []

    def test_api_response_format(self, client: TestClient):
        """Test that all API responses are valid JSON."""
        endpoints = ["/", "/health"]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            # Should be able to parse as JSON without errors
            data = response.json()
            assert isinstance(data, dict)

    def test_openapi_schema_available(self, client: TestClient):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        schema = response.json()

        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

        # Check that our endpoints are documented
        paths = schema["paths"]
        assert "/" in paths
        assert "/health" in paths
        assert "/inventory" in paths
        assert "/links/check" in paths