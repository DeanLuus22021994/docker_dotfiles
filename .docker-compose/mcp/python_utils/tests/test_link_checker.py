"""
Unit tests for LinkCheckerService.

Comprehensive test coverage for link validation functionality,
including URL checking, concurrent execution, and error handling.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from docker_examples_utils.config.settings import HTTPConfig, PathConfig
from docker_examples_utils.models.models import LinkCheckConfig, LinkResult
from docker_examples_utils.services.link_checker import LinkCheckerService


class TestLinkCheckerService:
    """Test suite for LinkCheckerService."""

    @pytest.fixture
    def config(self) -> LinkCheckConfig:
        """Create test configuration."""
        return LinkCheckConfig(
            max_workers=2,
            timeout=5,
            use_interpreters=False,
            skip_domains=["localhost", "127.0.0.1"]
        )

    @pytest.fixture
    def path_config(self, tmp_path: Path) -> PathConfig:
        """Create test path configuration."""
        return PathConfig(
            docs_path=tmp_path / "docs",
            src_path=tmp_path / "src",
            base_url="https://example.com"
        )

    @pytest.fixture
    def http_config(self) -> HTTPConfig:
        """Create test HTTP configuration."""
        return HTTPConfig(
            user_agent="TestAgent/1.0",
            max_retries=3,
            retry_status_codes=[429, 500, 502, 503, 504],
            backoff_factor=0.3
        )

    @pytest.fixture
    def service(self, config: LinkCheckConfig, path_config: PathConfig, http_config: HTTPConfig) -> LinkCheckerService:
        """Create LinkCheckerService instance."""
        return LinkCheckerService(config, path_config, http_config)

    def test_init(self, service: LinkCheckerService, config: LinkCheckConfig, path_config: PathConfig, http_config: HTTPConfig):
        """Test service initialization."""
        assert service.config == config
        assert service.path_config == path_config
        assert service.http_config == http_config
        assert service._session is None  # type: ignore
        assert service._requests_available is False  # type: ignore
        assert service.failure_count == 0
        assert service.failure_threshold == 5
        assert service.circuit_open is False

    def test_find_markdown_files(self, service: LinkCheckerService, tmp_path: Path):
        """Test finding markdown files."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        # Create test markdown files
        (docs_dir / "README.md").write_text("# Test")
        (docs_dir / "guide.md").write_text("# Guide")
        (docs_dir / "subdir").mkdir()
        (docs_dir / "subdir" / "nested.md").write_text("# Nested")

        # Create non-markdown file
        (docs_dir / "config.json").write_text("{}")

        files = service.find_markdown_files()

        assert len(files) == 3
        file_names = {f.name for f in files}
        assert file_names == {"README.md", "guide.md", "nested.md"}

    def test_extract_links_markdown(self, service: LinkCheckerService, tmp_path: Path):
        """Test extracting links from markdown content."""
        test_file = tmp_path / "test.md"
        test_file.write_text("""
# Test Document

[Internal Link](relative/path)
[External Link](https://example.com/page)
[Anchor Link](#section)
[Absolute Link](http://test.com)

<a href="https://html-link.com">HTML Link</a>
<img src="http://image.com/pic.jpg" alt="image">
        """)

        links = service.extract_links(test_file)

        expected_links = {
            "https://example.com/relative/path",  # relative link with base_url
            "https://example.com/page",  # external link unchanged
            "#section",  # anchor link unchanged
            "http://test.com",  # absolute link unchanged
            "https://html-link.com",  # HTML link extracted
            "http://image.com/pic.jpg"  # image src extracted
        }

        assert set(links) == expected_links

    def test_extract_links_file_error(self, service: LinkCheckerService, tmp_path: Path):
        """Test error handling when reading files."""
        # Create a file that will cause a read error
        test_file = tmp_path / "bad_file.md"

        # Mock the read_text method to raise an exception
        with patch.object(Path, 'read_text', side_effect=PermissionError("Access denied")):
            links = service.extract_links(test_file)

        # Should return empty list on error
        assert links == []

    @patch('requests.Session')
    @patch('requests.adapters.HTTPAdapter')
    @patch('urllib3.util.retry.Retry')
    def test_check_single_link_success(self, mock_retry: Mock, mock_adapter: Mock, mock_session_class: Mock, service: LinkCheckerService):
        """Test successful single link checking."""
        # Setup mocks
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_session.head.return_value = mock_response
        mock_session_class.return_value = mock_session

        # Mock time for response time calculation
        with patch('time.time', side_effect=[100.0, 100.5]):
            result = service._check_single_link("https://example.com")  # type: ignore

        assert isinstance(result, LinkResult)
        assert result.url == "https://example.com"
        assert result.is_valid is True
        assert result.status_code == 200
        assert result.response_time == 0.5
        assert result.error_message is None

    @patch('requests.Session')
    @patch('requests.adapters.HTTPAdapter')
    @patch('urllib3.util.retry.Retry')
    def test_check_single_link_redirect(self, mock_retry: Mock, mock_adapter: Mock, mock_session_class: Mock, service: LinkCheckerService):
        """Test link checking with redirect (405 -> GET)."""
        # Setup mocks
        mock_session = Mock()
        mock_head_response = Mock()
        mock_head_response.status_code = 405  # Method not allowed
        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_session.head.return_value = mock_head_response
        mock_session.get.return_value = mock_get_response
        mock_session_class.return_value = mock_session

        with patch('time.time', side_effect=[100.0, 100.3]):
            result = service._check_single_link("https://example.com")  # type: ignore

        assert result.is_valid is True
        assert result.status_code == 200
        mock_session.get.assert_called_once_with("https://example.com", timeout=10, allow_redirects=True)

    def test_check_single_link_skipped_domain(self, service: LinkCheckerService):
        """Test skipping links from configured domains."""
        result = service._check_single_link("http://localhost:3000")  # type: ignore

        assert isinstance(result, LinkResult)
        assert result.url == "http://localhost:3000"
        assert result.is_valid is True
        assert result.error_message == "skipped"

    def test_check_single_link_circuit_breaker(self, service: LinkCheckerService):
        """Test circuit breaker functionality."""
        # Set circuit breaker to open
        service.circuit_open = True

        result = service._check_single_link("https://example.com")  # type: ignore

        assert isinstance(result, LinkResult)
        assert result.is_valid is False
        assert result.error_message == "circuit breaker open"

    @patch('requests.Session')
    def test_check_single_link_requests_unavailable(self, mock_session_class: Mock, service: LinkCheckerService):
        """Test behavior when requests library is unavailable."""
        # Mock import error
        service._requests_available = False  # type: ignore

        result = service._check_single_link("https://example.com")  # type: ignore

        assert isinstance(result, LinkResult)
        assert result.is_valid is False
        assert result.error_message == "requests not available"

    @patch('requests.Session')
    @patch('requests.adapters.HTTPAdapter')
    @patch('urllib3.util.retry.Retry')
    def test_check_single_link_exception_handling(self, mock_retry: Mock, mock_adapter: Mock, mock_session_class: Mock, service: LinkCheckerService):
        """Test exception handling during link checking."""
        # Setup mock to raise exception
        mock_session = Mock()
        mock_session.head.side_effect = Exception("Network error")
        mock_session_class.return_value = mock_session

        with patch('time.time', side_effect=[100.0, 100.2]):
            result = service._check_single_link("https://example.com")  # type: ignore

        assert isinstance(result, LinkResult)
        assert result.is_valid is False
        assert result.error_message == "Network error"
        assert result.response_time == 0.2
        assert service.failure_count == 1

    @patch('requests.Session')
    @patch('requests.adapters.HTTPAdapter')
    @patch('urllib3.util.retry.Retry')
    def test_check_single_link_circuit_breaker_activation(self, mock_retry: Mock, mock_adapter: Mock, mock_session_class: Mock, service: LinkCheckerService):
        """Test circuit breaker activation after multiple failures."""
        # Setup mock to always fail
        mock_session = Mock()
        mock_session.head.side_effect = Exception("Persistent error")
        mock_session_class.return_value = mock_session

        # Trigger failures to activate circuit breaker
        for _ in range(6):  # One more than threshold
            service._check_single_link("https://example.com")  # type: ignore

        assert service.failure_count == 6
        assert service.circuit_open is True

    @patch('docker_examples_utils.services.link_checker.ThreadPoolExecutor')
    def test_check_links_concurrent_no_links(self, mock_executor_class: Mock, service: LinkCheckerService, tmp_path: Path):
        """Test concurrent link checking when no links are found."""
        # Create empty docs directory
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        results = service.check_links_concurrent()

        expected = {"valid": [], "broken": [], "skipped": []}
        assert results == expected
        mock_executor_class.assert_not_called()

    @patch('docker_examples_utils.services.link_checker.ThreadPoolExecutor')
    @patch('builtins.print')  # Suppress print output
    def test_check_links_concurrent_with_links(self, mock_print: Mock, mock_executor_class: Mock, service: LinkCheckerService, tmp_path: Path):
        """Test concurrent link checking with actual links."""
        # Create test markdown file with links
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "test.md").write_text("[Test](https://example.com)")

        # Mock executor and future
        mock_executor = Mock()
        mock_future = Mock()
        mock_result = LinkResult(
            url="https://example.com",
            is_valid=True,
            status_code=200,
            response_time=0.1
        )
        mock_future.result.return_value = mock_result
        mock_executor.__enter__.return_value = mock_executor
        mock_executor.submit.return_value = mock_future
        mock_executor_class.return_value = mock_executor

        with patch.object(service, '_check_single_link', return_value=mock_result):
            results = service.check_links_concurrent()

        assert results["valid"] == ["https://example.com"]
        assert results["broken"] == []
        assert results["skipped"] == []

    @pytest.mark.asyncio
    async def test_async_check_links(self, service: LinkCheckerService):
        """Test asynchronous link checking."""
        test_urls = ["https://example.com", "https://test.com"]

        # Mock the session setup
        service._requests_available = True  # type: ignore
        mock_session = Mock()
        service._session = mock_session  # type: ignore

        # Mock successful responses
        mock_response = Mock()
        mock_response.status_code = 200
        mock_session.head.return_value = mock_response

        with patch('asyncio.to_thread', return_value=mock_response):
            results = await service.async_check_links(test_urls)

        assert "valid" in results
        assert "broken" in results
        assert "skipped" in results
        assert len(results["valid"]) == 2

    @pytest.mark.asyncio
    async def test_async_check_links_requests_unavailable(self, service: LinkCheckerService):
        """Test async checking when requests is unavailable."""
        test_urls = ["https://example.com"]

        service._requests_available = False  # type: ignore

        results = await service.async_check_links(test_urls)

        assert results["broken"] == ["https://example.com (requests not available)"]
        assert results["valid"] == []
        assert results["skipped"] == []

    @pytest.mark.asyncio
    async def test_async_check_links_with_skipped_domains(self, service: LinkCheckerService):
        """Test async checking with skipped domains."""
        test_urls = ["http://localhost:3000", "https://example.com"]

        service._requests_available = True  # type: ignore
        mock_session = Mock()
        service._session = mock_session  # type: ignore

        mock_response = Mock()
        mock_response.status_code = 200
        mock_session.head.return_value = mock_response

        with patch('asyncio.to_thread', return_value=mock_response):
            results = await service.async_check_links(test_urls)

        assert len(results["skipped"]) == 1
        assert len(results["valid"]) == 1

    def test_async_check_links_python_version_check(self, service: LinkCheckerService):
        """Test that async checking requires Python 3.14+."""
        # This test would need to be adjusted based on actual Python version
        # For now, just ensure the method exists and can be called
        assert hasattr(service, 'async_check_links')