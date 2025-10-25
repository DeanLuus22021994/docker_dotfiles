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
    >>> from python.utils import success, error
    >>> from python.utils import read_json
    >>> from python.utils import setup_logger
"""

from . import colors, file_utils, logging_utils
from .colors import (
    Colors,
    bold,
    colorize,
    error,
    header,
    info,
    separator,
    success,
    warning,
)
from .file_utils import (
    ensure_dir,
    file_exists,
    get_file_size,
    get_files_by_extension,
    get_relative_path,
    read_json,
    read_lines,
    write_json,
)
from .logging_utils import ColoredFormatter, get_logger, setup_logger

__all__: list[str] = [
    # Submodules
    "colors",
    "file_utils",
    "logging_utils",
    # Colors
    "Colors",
    "colorize",
    "success",
    "warning",
    "error",
    "info",
    "bold",
    "header",
    "separator",
    # File utils
    "read_json",
    "write_json",
    "read_lines",
    "file_exists",
    "ensure_dir",
    "get_files_by_extension",
    "get_file_size",
    "get_relative_path",
    # Logging utils
    "ColoredFormatter",
    "setup_logger",
    "get_logger",
]
