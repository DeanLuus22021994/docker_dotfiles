#!/usr/bin/env python3
"""
Shared Logging Utilities Module

Provides centralized logging configuration with color-coded output support.
Implements custom formatters for improved log readability and debugging
across all Python scripts.

This module uses Python 3.14 type system features including Protocol, Literal,
Final, and TypeAlias for improved type safety and semantic clarity.

Examples:
    >>> from python.utils.logging_utils import setup_logger
    >>> logger = setup_logger('my_script', use_colors=True)
    >>> logger.info("Processing started")
"""

import logging
import sys
from typing import Final, Protocol

from python.types.aliases_colors import ColorCode
from python.types.aliases_logging import FormatString, LoggerName, LogLevel, LogLevelName
from python.types.constants.logging import DEFAULT_LOG_FORMAT
from python.types.enums import CRITICAL, DEBUG, ERROR, INFO, WARNING

from .colors import Colors

__all__: list[str] = [
    "ColoredFormatter",
    "setup_logger",
    "get_logger",
    "LogLevel",
    "LogLevelName",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
]


class FormatterProtocol(Protocol):
    """Protocol defining the interface for log formatters.

    Any class implementing this protocol can be used as a log formatter.
    Provides type safety for formatter objects in logging configuration.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record into a string.

        Args:
            record: Log record to format

        Returns:
            Formatted log message string
        """
        return ""  # Protocol method - implementation required in subclasses


class ColoredFormatter(logging.Formatter):
    """Custom formatter with ANSI color support.

    Automatically colorizes log level names based on severity.
    Uses immutable mapping for consistent color assignment.

    Attributes:
        LEVEL_COLORS: Immutable mapping of log levels to color codes

    Example:
        >>> formatter = ColoredFormatter("%(levelname)s: %(message)s")
        >>> handler.setFormatter(formatter)
    """

    LEVEL_COLORS: Final[dict[LogLevel, ColorCode]] = {
        logging.DEBUG: Colors.CYAN,
        logging.INFO: Colors.BLUE,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: f"{Colors.BOLD}{Colors.RED}",
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with appropriate color.

        Args:
            record: Log record to format

        Returns:
            Formatted and colorized log message
        """
        color = self.LEVEL_COLORS.get(record.levelno, Colors.RESET)
        record.levelname = f"{color}{record.levelname}{Colors.RESET}"
        return super().format(record)


def setup_logger(
    name: LoggerName,
    *,
    level: LogLevel = INFO,
    format_string: FormatString | None = None,
    use_colors: bool = True,
) -> logging.Logger:
    """Setup and configure logger with color support.

    Creates a new logger or reconfigures existing one with the specified
    settings. Automatically clears existing handlers to prevent duplication.

    Args:
        name: Logger name (typically __name__ or module name)
        level: Logging level (default: INFO). Use module constants:
               DEBUG, INFO, WARNING, ERROR, CRITICAL
        format_string: Custom format string (default: DEFAULT_FORMAT)
                      Supports standard logging format specifiers
        use_colors: Enable ANSI color output (default: True)
                   Automatically uses ColoredFormatter when True

    Returns:
        Configured logger instance ready for use

    Example:
        >>> logger = setup_logger(__name__, level=DEBUG, use_colors=True)
        >>> logger.debug("Debug message")  # Cyan colored
        >>> logger.info("Info message")   # Blue colored
        >>> logger.warning("Warning")      # Yellow colored
        >>> logger.error("Error occurred") # Red colored

    Note:
        If logger already exists, all handlers are cleared and reconfigured.
        This ensures consistent configuration across multiple setup calls.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to prevent duplication
    logger.handlers.clear()

    # Create console handler with same level
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Determine formatter based on color preference
    if format_string is None:
        format_string = DEFAULT_LOG_FORMAT

    formatter: FormatterProtocol
    if use_colors:
        formatter = ColoredFormatter(format_string)
    else:
        formatter = logging.Formatter(format_string)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_logger(name: LoggerName) -> logging.Logger:
    """Get existing logger instance.

    Retrieves logger by name without modifying configuration.
    If logger doesn't exist, creates basic logger with default settings.

    Args:
        name: Logger name to retrieve

    Returns:
        Logger instance (may be unconfigured if new)

    Example:
        >>> # After setup_logger(__name__) in module
        >>> logger = get_logger(__name__)
        >>> logger.info("Using existing logger")

    Note:
        Prefer using setup_logger() for initial configuration.
        Use get_logger() only when logger is already configured.
    """
    return logging.getLogger(name)
