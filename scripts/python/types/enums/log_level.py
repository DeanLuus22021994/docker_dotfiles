"""Log level enumeration."""

import logging
from enum import IntEnum
from typing import Final


class LogLevel(IntEnum):
    """Standard logging levels as enum."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


# Export as constants for direct use
DEBUG: Final[int] = LogLevel.DEBUG
INFO: Final[int] = LogLevel.INFO
WARNING: Final[int] = LogLevel.WARNING
ERROR: Final[int] = LogLevel.ERROR
CRITICAL: Final[int] = LogLevel.CRITICAL

__all__: list[str] = ["LogLevel", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
