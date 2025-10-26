"""Type stubs for colors module.

Provides type hints for ANSI color formatting utilities.
"""

from dataclasses import dataclass
from typing import Final, TypeAlias

# Type aliases
ColorCode: TypeAlias = str
AnsiCode: TypeAlias = str
FormattedText: TypeAlias = str

class Colors:
    """ANSI color codes for terminal output."""

    RESET: Final[ColorCode]
    BOLD: Final[AnsiCode]
    DIM: Final[AnsiCode]
    ITALIC: Final[AnsiCode]
    UNDERLINE: Final[AnsiCode]
    RED: Final[ColorCode]
    GREEN: Final[ColorCode]
    YELLOW: Final[ColorCode]
    BLUE: Final[ColorCode]
    MAGENTA: Final[ColorCode]
    CYAN: Final[ColorCode]
    WHITE: Final[ColorCode]

@dataclass(frozen=True, slots=True)
class ColorScheme:
    """Immutable color scheme for consistent styling."""

    success: ColorCode
    warning: ColorCode
    error: ColorCode
    info: ColorCode
    highlight: ColorCode

def colorize(_text: str, _color: ColorCode, /) -> FormattedText:
    """Apply color to text."""
    ...

def success(_text: str, /) -> FormattedText:
    """Format text as success (green with checkmark)."""
    ...

def warning(_text: str, /) -> FormattedText:
    """Format text as warning (yellow with warning symbol)."""
    ...

def error(_text: str, /) -> FormattedText:
    """Format text as error (red with X symbol)."""
    ...

def info(_text: str, /) -> FormattedText:
    """Format text as info (blue with info symbol)."""
    ...

def bold(_text: str, /) -> FormattedText:
    """Apply bold formatting to text."""
    ...

def header(_text: str, /) -> FormattedText:
    """Format text as header (bold blue)."""
    ...

def separator(width: int = 60, char: str = "=") -> FormattedText:
    """Create separator line."""
    ...

__all__: list[str]
