"""
Integration tests for CLI functionality.

Comprehensive test coverage for CLI argument parsing, command execution,
and integration with services.
"""

import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# pytest is used by the test framework but not directly imported
from cli.doc_utils_cli import main


class TestCLIArgumentParsing:
    """Test suite for CLI argument parsing."""

    def test_check_links_command_parsing(self) -> None:
        """Test parsing of check-links command."""
        with patch('sys.argv', ['doc_utils_cli', 'check-links']):
            with patch('cli.doc_utils_cli.LinkCheckerService') as mock_service:
                mock_instance = Mock()
                mock_instance.check_links_concurrent.return_value = {
                    "valid": ["http://example.com"],
                    "broken": [],
                    "skipped": []
                }
                mock_service.return_value = mock_instance

                result = main()
                assert result == 0
                mock_service.assert_called_once()

    def test_inventory_command_parsing(self) -> None:
        """Test parsing of inventory command."""
        with patch('sys.argv', ['doc_utils_cli', 'inventory']):
            with patch('cli.doc_utils_cli.ComponentInventoryService') as mock_service:
                mock_instance = Mock()
                mock_instance.generate_inventory.return_value = {
                    "pages": [],
                    "components": [],
                    "hooks": [],
                    "utils": []
                }
                mock_service.return_value = mock_instance

                result = main()
                assert result == 0
                mock_service.assert_called_once()

    def test_async_check_command_parsing(self) -> None:
        """Test parsing of async-check command."""
        with patch('sys.argv', ['doc_utils_cli', 'async-check']):
            with patch('cli.doc_utils_cli.LinkCheckerService') as mock_service:
                with patch('sys.version_info', (3, 14, 0)):
                    mock_instance = Mock()
                    async def mock_async_check(urls: list[str]) -> dict[str, list[str]]:
                        return {
                            "valid": ["http://example.com"],
                            "broken": [],
                            "skipped": []
                        }
                    mock_instance.async_check_links = mock_async_check
                    mock_service.return_value = mock_instance

                    result = main()
                    assert result == 0
                    mock_service.assert_called_once()

    def test_invalid_command(self) -> None:
        """Test handling of invalid command."""
        with patch('sys.argv', ['doc_utils_cli', 'invalid-command']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 2

    def test_workers_argument(self) -> None:
        """Test workers argument parsing."""
        with patch('sys.argv', ['doc_utils_cli', 'check-links', '--workers', '20']):
            with patch('cli.doc_utils_cli.LinkCheckerService') as mock_service:
                mock_instance = Mock()
                mock_instance.check_links_concurrent.return_value = {
                    "valid": [], "broken": [], "skipped": []
                }
                mock_service.return_value = mock_instance

                result = main()
                assert result == 0

                # Check that LinkCheckerService was called with correct config
                call_args = mock_service.call_args
                config = call_args[0][0]  # First positional argument
                assert config.max_workers == 20

    def test_docs_path_argument(self) -> None:
        """Test docs-path argument parsing."""
        with patch('sys.argv', ['doc_utils_cli', 'check-links', '--docs-path', '/custom/docs']):
            with patch('cli.doc_utils_cli.LinkCheckerService') as mock_service:
                mock_instance = Mock()
                mock_instance.check_links_concurrent.return_value = {
                    "valid": [], "broken": [], "skipped": []
                }
                mock_service.return_value = mock_instance

                result = main()
                assert result == 0

    def test_src_path_argument(self) -> None:
        """Test src-path argument parsing."""
        with patch('sys.argv', ['doc_utils_cli', 'inventory', '--src-path', '/custom/src']):
            with patch('cli.doc_utils_cli.ComponentInventoryService') as mock_service:
                mock_instance = Mock()
                mock_instance.generate_inventory.return_value = {
                    "pages": [], "components": [], "hooks": [], "utils": []
                }
                mock_service.return_value = mock_instance

                result = main()
                assert result == 0

                # Check that ComponentInventoryService was called with correct config
                call_args = mock_service.call_args
                config = call_args[0][0]  # First positional argument
                assert config.src_path == "/custom/src"

    def test_no_interpreters_flag(self) -> None:
        """Test no-interpreters flag."""
        with patch('sys.argv', ['doc_utils_cli', 'check-links', '--no-interpreters']):
            with patch('cli.doc_utils_cli.LinkCheckerService') as mock_service:
                mock_instance = Mock()
                mock_instance.check_links_concurrent.return_value = {
                    "valid": [], "broken": [], "skipped": []
                }
                mock_service.return_value = mock_instance

                result = main()
                assert result == 0

                # Check that LinkCheckerService was called with use_interpreters=False
                call_args = mock_service.call_args
                config = call_args[0][0]  # First positional argument
                assert config.use_interpreters is False

    def test_output_argument(self, tmp_path: Path):
        """Test output argument for saving results."""
        output_file = tmp_path / "results.json"
        with patch('sys.argv', ['doc_utils_cli', 'check-links', '--output', str(output_file)]):
            with patch('cli.doc_utils_cli.LinkCheckerService') as mock_service:
                mock_instance = Mock()
                test_results: dict[str, list[str]] = {
                    "valid": ["http://example.com"],
                    "broken": ["http://broken.com"],
                    "skipped": []
                }
                mock_instance.check_links_concurrent.return_value = test_results
                mock_service.return_value = mock_instance

                result = main()
                assert result == 0

                # Check that output file was created with correct content
                assert output_file.exists()
                with open(output_file, encoding='utf-8') as f:
                    saved_results = json.load(f)
                assert saved_results == test_results


class TestCLIIntegration:
    """Test suite for CLI integration with services."""

    @patch('cli.doc_utils_cli.LinkCheckerService')
    def test_check_links_integration(self, mock_service_class: Mock) -> None:
        """Test check-links command integration."""
        mock_instance = Mock()
        mock_instance.check_links_concurrent.return_value = {
            "valid": ["http://example.com", "http://test.com"],
            "broken": ["http://broken.com"],
            "skipped": ["mailto:test@example.com"]
        }
        mock_service_class.return_value = mock_instance

        with patch('sys.argv', ['doc_utils_cli', 'check-links']):
            result = main()

        assert result == 0
        mock_service_class.assert_called_once()
        mock_instance.check_links_concurrent.assert_called_once()

    @patch('cli.doc_utils_cli.ComponentInventoryService')
    def test_inventory_integration(self, mock_service_class: Mock) -> None:
        """Test inventory command integration."""
        mock_instance = Mock()
        mock_instance.generate_inventory.return_value = {
            "pages": [{"name": "test.md", "components": []}],
            "components": [{"name": "TestComponent", "type": "component"}],
            "hooks": [],
            "utils": [{"name": "test_utils.py", "functions": []}]
        }
        mock_service_class.return_value = mock_instance

        with patch('sys.argv', ['doc_utils_cli', 'inventory']):
            result = main()

        assert result == 0
        mock_service_class.assert_called_once()
        mock_instance.generate_inventory.assert_called_once()

    @patch('cli.doc_utils_cli.LinkCheckerService')
    @patch('sys.version_info', (3, 14, 0))
    def test_async_check_integration(self, mock_service_class: Mock) -> None:
        """Test async-check command integration with Python 3.14+."""
        mock_instance = Mock()
        async def mock_async_check(urls: list[str]) -> dict[str, list[str]]:
            return {
                "valid": ["http://example.com"],
                "broken": [],
                "skipped": []
            }
        mock_instance.async_check_links = mock_async_check
        mock_service_class.return_value = mock_instance

        with patch('sys.argv', ['doc_utils_cli', 'async-check']):
            result = main()

        assert result == 0
        mock_service_class.assert_called_once()
        # Note: async_check_links is called via asyncio.run, so we can't easily assert on it

    @patch('sys.version_info', (3, 13, 0))
    def test_async_check_python_version_error(self) -> None:
        """Test async-check command fails on Python < 3.14."""
        with patch('sys.argv', ['doc_utils_cli', 'async-check']):
            result = main()

        assert result == 0  # Should not crash, just print message

    def test_keyboard_interrupt_handling(self) -> None:
        """Test handling of KeyboardInterrupt."""
        with patch('sys.argv', ['doc_utils_cli', 'check-links']):
            with patch('cli.doc_utils_cli.LinkCheckerService') as mock_service:
                mock_instance = Mock()
                mock_instance.check_links_concurrent.side_effect = KeyboardInterrupt()
                mock_service.return_value = mock_instance

                result = main()
                assert result == 130  # Standard KeyboardInterrupt exit code

    def test_general_exception_handling(self) -> None:
        """Test handling of general exceptions."""
        with patch('sys.argv', ['doc_utils_cli', 'check-links']):
            with patch('cli.doc_utils_cli.LinkCheckerService') as mock_service:
                mock_instance = Mock()
                mock_instance.check_links_concurrent.side_effect = Exception("Test error")
                mock_service.return_value = mock_instance

                result = main()
                assert result == 1  # General error exit code


class TestCLIOutput:
    """Test suite for CLI output formatting and messages."""

    @patch('builtins.print')
    @patch('cli.doc_utils_cli.LinkCheckerService')
    def test_check_links_output(self, mock_service_class: Mock, mock_print: Mock) -> None:
        """Test check-links command output formatting."""
        mock_instance = Mock()
        mock_instance.check_links_concurrent.return_value = {
            "valid": ["http://example.com"],
            "broken": ["http://broken.com"],
            "skipped": []
        }
        mock_service_class.return_value = mock_instance

        with patch('sys.argv', ['doc_utils_cli', 'check-links']):
            result = main()

        assert result == 0

        # Check that output contains expected messages
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert any("🔗 Checking documentation links..." in msg for msg in print_calls)
        assert any("✅ Valid links: 1" in msg for msg in print_calls)
        assert any("❌ Broken links: 1" in msg for msg in print_calls)
        assert any("⏭️  Skipped links: 0" in msg for msg in print_calls)

    @patch('builtins.print')
    @patch('cli.doc_utils_cli.ComponentInventoryService')
    def test_inventory_output(self, mock_service_class: Mock, mock_print: Mock) -> None:
        """Test inventory command output formatting."""
        mock_instance = Mock()
        mock_instance.generate_inventory.return_value = {
            "pages": [{"name": "test.md"}],
            "components": [{"name": "TestComponent"}],
            "hooks": [],
            "utils": [{"name": "test_utils.py"}]
        }
        mock_service_class.return_value = mock_instance

        with patch('sys.argv', ['doc_utils_cli', 'inventory']):
            result = main()

        assert result == 0

        # Check that output contains expected messages
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert any("📦 Generating component inventory..." in msg for msg in print_calls)
        assert any("📄 Pages: 1" in msg for msg in print_calls)
        assert any("🧩 Components: 1" in msg for msg in print_calls)
        assert any("🪝 Hooks: 0" in msg for msg in print_calls)
        assert any("🛠️  Utils: 1" in msg for msg in print_calls)


class TestCLIConfiguration:
    """Test suite for CLI configuration handling."""

    @patch('cli.doc_utils_cli.has_interpreters')
    @patch('cli.doc_utils_cli.LinkCheckerService')
    def test_interpreter_detection(self, mock_service_class: Mock, mock_has_interpreters: Mock) -> None:
        """Test interpreter detection and usage."""
        mock_has_interpreters.return_value = True
        mock_instance = Mock()
        mock_instance.check_links_concurrent.return_value = {
            "valid": [], "broken": [], "skipped": []
        }
        mock_service_class.return_value = mock_instance

        with patch('sys.argv', ['doc_utils_cli', 'check-links']):
            result = main()

        assert result == 0

        # Check that LinkCheckerService was called with use_interpreters=True
        call_args = mock_service_class.call_args
        config = call_args[0][0]  # First positional argument
        assert config.use_interpreters is True

    @patch('cli.doc_utils_cli.has_interpreters')
    @patch('cli.doc_utils_cli.LinkCheckerService')
    def test_no_interpreters_fallback(self, mock_service_class: Mock, mock_has_interpreters: Mock) -> None:
        """Test fallback when interpreters are not available."""
        mock_has_interpreters.return_value = False
        mock_instance = Mock()
        mock_instance.check_links_concurrent.return_value = {
            "valid": [], "broken": [], "skipped": []
        }
        mock_service_class.return_value = mock_instance

        with patch('sys.argv', ['doc_utils_cli', 'check-links']):
            result = main()

        assert result == 0

        # Check that LinkCheckerService was called with use_interpreters=False
        call_args = mock_service_class.call_args
        config = call_args[0][0]  # First positional argument
        assert config.use_interpreters is False

    def test_python_version_display(self) -> None:
        """Test that Python version is displayed."""
        with patch('sys.argv', ['doc_utils_cli', 'check-links']):
            with patch('builtins.print') as mock_print:
                with patch('cli.doc_utils_cli.LinkCheckerService') as mock_service:
                    mock_instance = Mock()
                    mock_instance.check_links_concurrent.return_value = {
                        "valid": [], "broken": [], "skipped": []
                    }
                    mock_service.return_value = mock_instance

                    result = main()

        assert result == 0

        # Check that Python version is printed
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert any(f"🐍 Python {sys.version}" in msg for msg in print_calls)

    def test_executor_type_display(self) -> None:
        """Test that executor type is displayed."""
        with patch('sys.argv', ['doc_utils_cli', 'check-links']):
            with patch('builtins.print') as mock_print:
                with patch('cli.doc_utils_cli.LinkCheckerService') as mock_service:
                    mock_instance = Mock()
                    mock_instance.check_links_concurrent.return_value = {
                        "valid": [], "broken": [], "skipped": []
                    }
                    mock_service.return_value = mock_instance

                    result = main()

        assert result == 0

        # Check that executor type is printed
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert any("🔧 Using" in msg and "Executor" in msg for msg in print_calls)
