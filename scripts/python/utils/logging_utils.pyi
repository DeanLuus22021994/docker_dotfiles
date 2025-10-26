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
    
    def format(self, record: logging.LogRecord) -> str: ...

class ColoredFormatter(logging.Formatter):
    """Custom formatter with ANSI color support."""
    
    LEVEL_COLORS: Final[dict[LogLevel, ColorCode]]
    
    def format(self, record: logging.LogRecord) -> str: ...

def setup_logger(
    name: LoggerName,
    *,
    level: LogLevel = INFO,
    format_string: FormatString | None = None,
    use_colors: bool = True,
) -> logging.Logger:
    """Setup and configure logger with color support."""
    ...

def get_logger(name: LoggerName) -> logging.Logger:
    """Get existing logger instance."""
    ...

__all__: list[str]
