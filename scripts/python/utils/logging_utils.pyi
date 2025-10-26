"""Type stubs for logging_utils module.

Provides type hints for logging configuration utilities.
"""

import logging
from typing import Final, Literal, Protocol, TypeAlias

from .colors import ColorCode

# Type aliases
LogLevel: TypeAlias = int
LogLevelName: TypeAlias = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
FormatString: TypeAlias = str
LoggerName: TypeAlias = str

# Log level constants
DEBUG: Final[LogLevel]
INFO: Final[LogLevel]
WARNING: Final[LogLevel]
ERROR: Final[LogLevel]
CRITICAL: Final[LogLevel]

# Default format
DEFAULT_FORMAT: Final[FormatString]

class FormatterProtocol(Protocol):
    """Protocol for log formatters."""

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record to string."""
        pass

class ColoredFormatter(logging.Formatter):
    """Custom formatter with color-coded log levels."""

    level_colors: dict[LogLevelName, ColorCode]

    def __init__(self, fmt: FormatString | None = None, use_colors: bool = True) -> None: ...

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        pass

def setup_logger(
    name: LoggerName,
    /,
    *,
    level: LogLevel = 20,
    format_string: FormatString | None = None,
    use_colors: bool = True,
) -> logging.Logger:
    """Configure and return a logger with colored output."""
    pass

def get_logger(name: LoggerName, /) -> logging.Logger:
    """Get or create a logger instance."""
    pass

__all__: list[str]
