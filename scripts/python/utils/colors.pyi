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

def colorize(text: str, color: ColorCode, /) -> FormattedText:
    """Apply color to text."""
    pass

def success(text: str, /) -> FormattedText:
    """Format text as success (green with checkmark)."""
    pass

def warning(text: str, /) -> FormattedText:
    """Format text as warning (yellow with warning symbol)."""
    pass

def error(text: str, /) -> FormattedText:
    """Format text as error (red with X symbol)."""
    pass

def info(text: str, /) -> FormattedText:
    """Format text as info (blue with info symbol)."""
    pass

def bold(text: str, /) -> FormattedText:
    """Apply bold formatting to text."""
    pass

def header(text: str, /) -> FormattedText:
    """Format text as header (bold blue)."""
    pass

def separator(width: int = 60, char: str = "=") -> FormattedText:
    """Create separator line."""
    pass

__all__: list[str]
