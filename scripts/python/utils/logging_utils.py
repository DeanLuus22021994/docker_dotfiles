#!/usr/bin/env python3
"""
Shared Logging Utilities Module

Provides centralized logging configuration with color-coded output support.
Implements custom formatters for improved log readability and debugging
across all Python scripts.

Examples:
    >>> from python.utils.logging_utils import setup_logger
    >>> logger = setup_logger('my_script', use_colors=True)
    >>> logger.info("Processing started")
"""

__all__: list[str] = [
    "ColoredFormatter",
    "setup_logger",
    "get_logger",
]

import logging
import sys
from typing import Optional

from .colors import Colors


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support"""

    LEVEL_COLORS = {
        logging.DEBUG: Colors.CYAN,
        logging.INFO: Colors.BLUE,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: f"{Colors.BOLD}{Colors.RED}",
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with color"""
        color = self.LEVEL_COLORS.get(record.levelno, Colors.RESET)
        record.levelname = f"{color}{record.levelname}{Colors.RESET}"
        return super().format(record)


def setup_logger(
    name: str,
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    use_colors: bool = True,
) -> logging.Logger:
    """
    Setup and configure logger

    Args:
        name: Logger name
        level: Logging level (default: INFO)
        format_string: Custom format string (default: '%(levelname)s: %(message)s')
        use_colors: Use colored output (default: True)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Create formatter
    if format_string is None:
        format_string = "%(levelname)s: %(message)s"

    if use_colors:
        formatter: logging.Formatter = ColoredFormatter(format_string)
    else:
        formatter = logging.Formatter(format_string)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get existing logger or create basic one

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
