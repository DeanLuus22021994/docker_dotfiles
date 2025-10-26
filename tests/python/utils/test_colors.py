"""Tests for colors module."""

import pytest

from scripts.python.utils.colors import (
    Colors,
    bold,
    colorize,
    error,
    header,
    info,
    separator,
    success,
    warning,
)


class TestColors:
    """Test Colors class ANSI codes."""

    def test_colors_defined(self) -> None:
        """Test all color codes are defined."""
        assert Colors.GREEN == "\033[92m"
        assert Colors.YELLOW == "\033[93m"
        assert Colors.RED == "\033[91m"
        assert Colors.BLUE == "\033[94m"
        assert Colors.MAGENTA == "\033[95m"
        assert Colors.CYAN == "\033[96m"
        assert Colors.WHITE == "\033[97m"
        assert Colors.RESET == "\033[0m"
        assert Colors.BOLD == "\033[1m"
        assert Colors.DIM == "\033[2m"
        assert Colors.ITALIC == "\033[3m"
        assert Colors.UNDERLINE == "\033[4m"


class TestColorize:
    """Test colorize function."""

    def test_colorize_basic(self) -> None:
        """Test basic colorization."""
        result = colorize("test", Colors.GREEN)
        assert result == f"{Colors.GREEN}test{Colors.RESET}"

    def test_colorize_empty_string(self) -> None:
        """Test colorizing empty string."""
        result = colorize("", Colors.RED)
        assert result == f"{Colors.RED}{Colors.RESET}"

    def test_colorize_multiline(self) -> None:
        """Test colorizing multiline text."""
        text = "line1\nline2\nline3"
        result = colorize(text, Colors.BLUE)
        assert result == f"{Colors.BLUE}{text}{Colors.RESET}"

    def test_colorize_special_characters(self) -> None:
        """Test colorizing text with special characters."""
        text = "✓ ⚠ ✗ ℹ"
        result = colorize(text, Colors.CYAN)
        assert result == f"{Colors.CYAN}{text}{Colors.RESET}"


class TestSuccessWarningErrorInfo:
    """Test message formatting functions."""

    def test_success(self) -> None:
        """Test success message formatting."""
        result = success("Operation completed")
        assert "✓ Operation completed" in result
        assert Colors.GREEN in result
        assert Colors.RESET in result

    def test_warning(self) -> None:
        """Test warning message formatting."""
        result = warning("Careful now")
        assert "⚠ Careful now" in result
        assert Colors.YELLOW in result
        assert Colors.RESET in result

    def test_error(self) -> None:
        """Test error message formatting."""
        result = error("Something failed")
        assert "✗ Something failed" in result
        assert Colors.RED in result
        assert Colors.RESET in result

    def test_info(self) -> None:
        """Test info message formatting."""
        result = info("For your information")
        assert "ℹ For your information" in result
        assert Colors.BLUE in result
        assert Colors.RESET in result

    def test_empty_messages(self) -> None:
        """Test functions with empty strings."""
        assert "✓ " in success("")
        assert "⚠ " in warning("")
        assert "✗ " in error("")
        assert "ℹ " in info("")


class TestBold:
    """Test bold text function."""

    def test_bold(self) -> None:
        """Test bold text formatting."""
        result = bold("Important")
        assert result == f"{Colors.BOLD}Important{Colors.RESET}"

    def test_bold_empty(self) -> None:
        """Test bold with empty string."""
        result = bold("")
        assert result == f"{Colors.BOLD}{Colors.RESET}"


class TestHeader:
    """Test header function."""

    def test_header(self) -> None:
        """Test header formatting."""
        result = header("Section Title")
        assert Colors.BOLD in result
        assert Colors.BLUE in result
        assert "Section Title" in result
        assert Colors.RESET in result

    def test_header_empty(self) -> None:
        """Test header with empty string."""
        result = header("")
        assert Colors.BOLD in result
        assert Colors.BLUE in result
        assert Colors.RESET in result


class TestSeparator:
    """Test separator function."""

    def test_separator_default(self) -> None:
        """Test separator with default parameters."""
        result = separator()
        assert Colors.BOLD in result
        assert Colors.RESET in result
        assert "=" * 60 in result

    def test_separator_custom_width(self) -> None:
        """Test separator with custom width."""
        result = separator(width=20)
        assert "=" * 20 in result

    def test_separator_custom_char(self) -> None:
        """Test separator with custom character."""
        result = separator(char="-")
        assert "-" * 60 in result

    def test_separator_both_custom(self) -> None:
        """Test separator with both custom parameters."""
        result = separator(width=10, char="*")
        assert "*" * 10 in result

    @pytest.mark.parametrize("width", [0, 1, 5, 100])
    def test_separator_various_widths(self, width: int) -> None:
        """Test separator with various widths."""
        result = separator(width=width)
        assert "=" * width in result

    @pytest.mark.parametrize("char", ["=", "-", "*", "#", "~"])
    def test_separator_various_chars(self, char: str) -> None:
        """Test separator with various characters."""
        result = separator(char=char)
        assert char * 60 in result
