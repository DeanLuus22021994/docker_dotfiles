"""
Python Utilities Package

Shared utility modules providing DRY (Don't Repeat Yourself) functionality
across all Python scripts. Contains color formatting, file operations,
and logging configuration helpers.

Submodules:
    colors: ANSI color codes and terminal formatting functions
    file_utils: File I/O and path management utilities
    logging_utils: Logging configuration with color support

Examples:
    >>> from python.utils.colors import success, error
    >>> from python.utils.file_utils import read_json
    >>> from python.utils.logging_utils import setup_logger
"""

from . import colors, file_utils, logging_utils

__all__: list[str] = ["colors", "file_utils", "logging_utils"]
