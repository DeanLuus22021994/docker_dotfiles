#!/usr/bin/env python3
"""
Shared Colors Utility Module

Provides ANSI color codes and utility functions for terminal output formatting.
Supports modern terminals with 256-color capability and provides consistent
color schemes across all Python scripts.

This module uses Python 3.14 type system features including TypeAlias, Final,
and dataclasses for improved type safety and semantic indexing.

Examples:
    >>> from python.utils.colors import success, error, warning
    >>> print(success("Operation completed"))
    ✓ Operation completed
    >>> print(error("Something failed"))
    ✗ Something failed
"""

from dataclasses import dataclass
from typing import Final, TypeAlias

# Type aliases for semantic clarity
ColorCode: TypeAlias = str
AnsiCode: TypeAlias = str
FormattedText: TypeAlias = str

__all__: list[str] = [
    "Colors",
    "ColorScheme",
    "colorize",
    "success",
    "warning",
    "error",
    "info",
    "bold",
    "header",
    "separator",
    "ColorCode",
    "FormattedText",
]


class Colors:
    """ANSI color codes for terminal output.

    All constants are immutable (Final) to prevent accidental modification
    and ensure consistent formatting across the application.
    """

    GREEN: Final[ColorCode] = "\033[92m"
    YELLOW: Final[ColorCode] = "\033[93m"
    RED: Final[ColorCode] = "\033[91m"
    BLUE: Final[ColorCode] = "\033[94m"
    MAGENTA: Final[ColorCode] = "\033[95m"
    CYAN: Final[ColorCode] = "\033[96m"
    WHITE: Final[ColorCode] = "\033[97m"
    RESET: Final[AnsiCode] = "\033[0m"
    BOLD: Final[AnsiCode] = "\033[1m"
    DIM: Final[AnsiCode] = "\033[2m"
    ITALIC: Final[AnsiCode] = "\033[3m"
    UNDERLINE: Final[AnsiCode] = "\033[4m"


@dataclass(frozen=True, slots=True)
class ColorScheme:
    """Immutable color scheme for consistent theming.

    Attributes:
        success: Color for success messages (default: GREEN)
        warning: Color for warning messages (default: YELLOW)
        error: Color for error messages (default: RED)
        info: Color for informational messages (default: BLUE)
        highlight: Color for highlighted text (default: CYAN)

    Example:
        >>> scheme = ColorScheme()
        >>> print(colorize("Success", scheme.success))
    """

    success: ColorCode = Colors.GREEN
    warning: ColorCode = Colors.YELLOW
    error: ColorCode = Colors.RED
    info: ColorCode = Colors.BLUE
    highlight: ColorCode = Colors.CYAN


def colorize(text: str, color: ColorCode) -> FormattedText:
    """Wrap text with ANSI color codes.

    Args:
        text: Text to colorize
        color: ANSI color code (e.g., Colors.GREEN)

    Returns:
        Text wrapped with color codes and automatic reset

    Example:
        >>> colorize("Hello", Colors.GREEN)
        '\\033[92mHello\\033[0m'
    """
    return f"{color}{text}{Colors.RESET}"


def success(text: str) -> FormattedText:
    """Format text as success message with checkmark.

    Args:
        text: Message content

    Returns:
        Green colored text with ✓ prefix
    """
    return colorize(f"✓ {text}", Colors.GREEN)


def warning(text: str) -> FormattedText:
    """Format text as warning message.

    Args:
        text: Warning content

    Returns:
        Yellow colored text with ⚠ prefix
    """
    return colorize(f"⚠ {text}", Colors.YELLOW)


def error(text: str) -> FormattedText:
    """Format text as error message.

    Args:
        text: Error content

    Returns:
        Red colored text with ✗ prefix
    """
    return colorize(f"✗ {text}", Colors.RED)


def info(text: str) -> FormattedText:
    """Format text as informational message.

    Args:
        text: Info content

    Returns:
        Blue colored text with ℹ prefix
    """
    return colorize(f"ℹ {text}", Colors.BLUE)


def bold(text: str) -> FormattedText:
    """Format text as bold.

    Args:
        text: Text to make bold

    Returns:
        Bold formatted text
    """
    return colorize(text, Colors.BOLD)


def header(text: str) -> FormattedText:
    """Format text as bold blue header.

    Args:
        text: Header text

    Returns:
        Bold blue formatted text
    """
    return colorize(text, f"{Colors.BOLD}{Colors.BLUE}")


def separator(width: int = 60, char: str = "=") -> FormattedText:
    """Create a bold separator line.

    Args:
        width: Line width in characters (default: 60)
        char: Character to repeat (default: '=')

    Returns:
        Bold formatted separator line

    Example:
        >>> separator(40, '-')
        '\\033[1m----------------------------------------\\033[0m'
    """
    return colorize(char * width, Colors.BOLD)
