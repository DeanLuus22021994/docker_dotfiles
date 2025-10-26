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
    RED: Final[ColorCode]
    GREEN: Final[ColorCode]
    YELLOW: Final[ColorCode]
    BLUE: Final[ColorCode]
    MAGENTA: Final[ColorCode]
    CYAN: Final[ColorCode]
    WHITE: Final[ColorCode]
    
    def __init__(self) -> None: ...

@dataclass(frozen=True, slots=True)
class ColorScheme:
    """Immutable color scheme for consistent styling."""
    
    success: ColorCode
    warning: ColorCode
    error: ColorCode
    info: ColorCode
    highlight: ColorCode
    
    def __init__(
        self,
        success: ColorCode = ...,
        warning: ColorCode = ...,
        error: ColorCode = ...,
        info: ColorCode = ...,
        highlight: ColorCode = ...,
    ) -> None: ...

def colorize(text: str, color: ColorCode) -> FormattedText:
    """Apply color to text."""
    ...

def success(text: str) -> FormattedText:
    """Format text as success (green with checkmark)."""
    ...

def warning(text: str) -> FormattedText:
    """Format text as warning (yellow with warning symbol)."""
    ...

def error(text: str) -> FormattedText:
    """Format text as error (red with X symbol)."""
    ...

def info(text: str) -> FormattedText:
    """Format text as info (blue with info symbol)."""
    ...

def bold(text: str) -> FormattedText:
    """Apply bold formatting to text."""
    ...

def header(text: str) -> FormattedText:
    """Format text as header (bold blue)."""
    ...

def separator(length: int = 80, char: str = "=") -> FormattedText:
    """Create separator line."""
    ...

__all__: list[str]
