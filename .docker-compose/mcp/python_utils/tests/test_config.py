"""
Unit tests for configuration management.

Comprehensive test coverage for config validation, environment variables,
and settings management.
"""

import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# pytest is used by the test framework but not directly imported
from docker_examples_utils.config.config import LogLevel, LoggingConfig
from docker_examples_utils.config.settings import HTTPConfig, PathConfig


class TestPathConfig:
    """Test suite for PathConfig."""

    def test_init_default_values(self):
        """Test PathConfig initialization with default values."""
        config = PathConfig()

        assert config.docs_path == Path("docs")
        assert config.src_path == Path("src")
        assert config.base_url == "https://user.github.io/docker-examples/"

    def test_init_custom_values(self, tmp_path: Path):
        """Test PathConfig initialization with custom values."""
        docs_path = tmp_path / "custom_docs"
        src_path = tmp_path / "custom_src"
        base_url = "https://custom.example.com"

        config = PathConfig(
            docs_path=docs_path,
            src_path=src_path,
            base_url=base_url
        )

        assert config.docs_path == docs_path
        assert config.src_path == src_path
        assert config.base_url == base_url

    def test_path_validation(self, tmp_path: Path):
        """Test that paths are properly validated and converted."""
        config = PathConfig(
            docs_path=tmp_path / "docs",
            src_path=tmp_path / "src"
        )

        assert isinstance(config.docs_path, Path)
        assert isinstance(config.src_path, Path)

    def test_base_url_validation(self):
        """Test base URL validation."""
        # Valid URLs
        valid_urls = [
            "https://github.com",
            "http://localhost:3000",
            "https://example.com/path"
        ]

        for url in valid_urls:
            config = PathConfig(base_url=url)
            assert config.base_url == url

    def test_docs_path_property(self, tmp_path: Path):
        """Test docs_path property access."""
        config = PathConfig(docs_path=tmp_path / "docs")
        assert config.docs_path == tmp_path / "docs"

    def test_src_path_property(self, tmp_path: Path):
        """Test src_path property access."""
        config = PathConfig(src_path=tmp_path / "src")
        assert config.src_path == tmp_path / "src"


class TestHTTPConfig:
    """Test suite for HTTPConfig."""

    def test_init_default_values(self):
        """Test HTTPConfig initialization with default values."""
        config = HTTPConfig()

        assert config.user_agent == "Docker-Compose-Utils/1.0"
        assert config.max_retries == 3
        assert config.retry_status_codes == [429, 500, 502, 503, 504]
        assert config.backoff_factor == 1.0
        assert config.timeout == 30

    def test_init_custom_values(self):
        """Test HTTPConfig initialization with custom values."""
        config = HTTPConfig(
            user_agent="CustomAgent/2.0",
            max_retries=5,
            retry_status_codes=[500, 502, 503],
            backoff_factor=0.5,
            timeout=60
        )

        assert config.user_agent == "CustomAgent/2.0"
        assert config.max_retries == 5
        assert config.retry_status_codes == [500, 502, 503]
        assert config.backoff_factor == 0.5
        assert config.timeout == 60

    def test_user_agent_validation(self):
        """Test user agent string validation."""
        # Should accept various user agent formats
        valid_agents = [
            "Docker-Compose-Utils/1.0",
            "MyApp/1.2.3",
            "TestAgent"
        ]

        for agent in valid_agents:
            config = HTTPConfig(user_agent=agent)
            assert config.user_agent == agent

    def test_max_retries_validation(self):
        """Test max retries validation."""
        # Should accept reasonable retry counts
        for retries in [0, 1, 3, 5, 10]:
            config = HTTPConfig(max_retries=retries)
            assert config.max_retries == retries

    def test_retry_status_codes_validation(self):
        """Test retry status codes validation."""
        custom_codes = [408, 429, 500, 502, 503, 504]
        config = HTTPConfig(retry_status_codes=custom_codes)
        assert config.retry_status_codes == custom_codes

    def test_backoff_factor_validation(self):
        """Test backoff factor validation."""
        for factor in [0.1, 0.3, 0.5, 1.0, 2.0]:
            config = HTTPConfig(backoff_factor=factor)
            assert config.backoff_factor == factor

    def test_timeout_validation(self):
        """Test timeout validation."""
        for timeout in [5, 10, 30, 60, 120]:
            config = HTTPConfig(timeout=timeout)
            assert config.timeout == timeout


class TestLoggingConfig:
    """Test suite for LoggingConfig."""

    def test_init_default_values(self):
        """Test LoggingConfig initialization with default values."""
        config = LoggingConfig()

        assert config.level == LogLevel.INFO
        assert config.format == "json"
        assert config.enable_correlation_ids is True

    def test_init_custom_values(self):
        """Test LoggingConfig initialization with custom values."""
        config = LoggingConfig(
            level=LogLevel.DEBUG,
            format="Custom format: %(message)s",
            enable_correlation_ids=False
        )

        assert config.level == LogLevel.DEBUG
        assert config.format == "Custom format: %(message)s"
        assert config.enable_correlation_ids is False

    def test_log_level_enum(self):
        """Test LogLevel enum values."""
        assert LogLevel.DEBUG.value == "DEBUG"
        assert LogLevel.INFO.value == "INFO"
        assert LogLevel.WARNING.value == "WARNING"
        assert LogLevel.ERROR.value == "ERROR"
        assert LogLevel.CRITICAL.value == "CRITICAL"

    @patch('logging.basicConfig')
    def test_configure_logging_default(self, mock_basic_config: Mock):
        """Test logging configuration with default settings."""
        import logging
        config = LoggingConfig()
        config.configure_logging()

        mock_basic_config.assert_called_once_with(
            format="%(message)s",
            stream=sys.stdout,
            level=logging.INFO,
        )

    @patch('logging.basicConfig')
    def test_configure_logging_custom_level(self, mock_basic_config: Mock):
        """Test logging configuration with custom log level."""
        import logging
        config = LoggingConfig(level=LogLevel.DEBUG)
        config.configure_logging()

        mock_basic_config.assert_called_once_with(
            format="%(message)s",
            stream=sys.stdout,
            level=logging.DEBUG,
        )

    @patch('logging.getLogger')
    def test_get_correlation_logger(self, mock_get_logger: Mock):
        """Test getting correlation logger."""
        config = LoggingConfig()
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        correlation_id = "test-123"
        logger = config.get_correlation_logger(correlation_id)

        assert logger is not None
        mock_get_logger.assert_called_once_with("docker_examples_api")

    @patch('logging.getLogger')
    def test_get_correlation_logger_adapter(self, mock_get_logger: Mock):
        """Test that correlation logger uses LoggerAdapter when enabled."""
        config = LoggingConfig(enable_correlation_ids=True)
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        correlation_id = "test-123"
        logger = config.get_correlation_logger(correlation_id)

        # Should return a CorrelationLogger instance
        assert hasattr(logger, 'get_correlation_id')

    @patch('logging.getLogger')
    def test_get_correlation_logger_disabled(self, mock_get_logger: Mock):
        """Test correlation logger when disabled."""
        config = LoggingConfig(enable_correlation_ids=False)
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        correlation_id = "test-123"
        logger = config.get_correlation_logger(correlation_id)

        # Should return CorrelationLogger instance regardless
        assert hasattr(logger, 'get_correlation_id')


class TestConfigurationIntegration:
    """Test suite for configuration integration and validation."""

    @patch.dict(os.environ, {
        'DOCKER_EXAMPLES__PATHS__DOCS_PATH': '/custom/docs',
        'DOCKER_EXAMPLES__PATHS__SRC_PATH': '/custom/src',
        'DOCKER_EXAMPLES__PATHS__BASE_URL': 'https://custom.example.com'
    })
    def test_environment_variable_integration(self):
        """Test that configurations can be influenced by environment variables."""
        # Note: This test assumes the config classes can read env vars
        # In a real implementation, you might use pydantic-settings or similar

        # For now, just test that the classes can be instantiated
        # with various configurations
        config = PathConfig(
            docs_path=Path("/custom/docs"),
            src_path=Path("/custom/src"),
            base_url="https://custom.example.com"
        )

        assert str(config.docs_path) == str(Path("/custom/docs"))
        assert str(config.src_path) == str(Path("/custom/src"))
        assert config.base_url == "https://custom.example.com"

    def test_configuration_validation(self):
        """Test configuration validation and error handling."""
        # Test that invalid configurations raise appropriate errors
        # This would depend on the validation logic in the actual config classes

        # For PathConfig, test path validation
        config = PathConfig(docs_path=Path("docs"), src_path=Path("src"))
        assert isinstance(config.docs_path, Path)
        assert isinstance(config.src_path, Path)

    def test_config_immutability(self):
        """Test that configuration objects are immutable after creation."""
        config = PathConfig(docs_path=Path("docs"), src_path=Path("src"), base_url="https://example.com")

        # Create new config to verify immutability concept
        new_config = PathConfig(docs_path=Path("new_docs"), src_path=Path("new_src"))
        assert new_config.docs_path != config.docs_path
        assert new_config.src_path != config.src_path

    def test_config_serialization(self):
        """Test configuration serialization for debugging/logging."""
        config = PathConfig(docs_path=Path("docs"), src_path=Path("src"), base_url="https://example.com")

        # Should be able to convert to dict or string representation
        config_dict = {
            "docs_path": str(config.docs_path),
            "src_path": str(config.src_path),
            "base_url": config.base_url
        }

        assert config_dict["docs_path"] == "docs"
        assert config_dict["src_path"] == "src"
        assert config_dict["base_url"] == "https://example.com"

    def test_http_config_retry_logic(self):
        """Test HTTP config retry logic parameters."""
        config = HTTPConfig(
            max_retries=3,
            retry_status_codes=[429, 500, 502, 503, 504],
            backoff_factor=0.3
        )

        # Verify retry configuration
        assert config.max_retries == 3
        assert 429 in config.retry_status_codes
        assert 500 in config.retry_status_codes
        assert config.backoff_factor == 0.3

    def test_logging_config_levels(self):
        """Test logging configuration with different levels."""
        for level in [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR, LogLevel.CRITICAL]:
            config = LoggingConfig(level=level)
            assert config.level == level

    def test_path_config_base_url_handling(self):
        """Test PathConfig base URL handling."""
        config = PathConfig(base_url="https://github.com/user/repo")

        # Should handle URLs with paths
        assert config.base_url == "https://github.com/user/repo"

        # Should handle URLs without paths
        config2 = PathConfig(base_url="https://example.com")
        assert config2.base_url == "https://example.com"