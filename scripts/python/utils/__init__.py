"""
Python Utilities Package

Shared utility modules providing DRY (Don't Repeat Yourself) functionality
across all Python scripts with Python 3.14 type system features.

Submodules:
    colors: ANSI color codes, ColorScheme dataclass, and formatting functions
    file_utils: File I/O with PathLike support and semantic types
    logging_utils: Logging configuration with Protocol and Literal types

Examples:
    >>> from python.utils import success, error, ColorScheme
    >>> from python.utils import read_json, StrPath
    >>> from python.utils import setup_logger, LogLevel
"""

from . import colors, file_utils, logging_utils

# Colors module exports
from .colors import (
    AnsiCode,
    ColorCode,
    Colors,
    ColorScheme,
    FormattedText,
    bold,
    colorize,
    error,
    header,
    info,
    separator,
    success,
    warning,
)

# File utils module exports
from .file_utils import (
    DEFAULT_ENCODING,
    DEFAULT_JSON_INDENT,
    FileSize,
    JSONDict,
    StrPath,
    ensure_dir,
    file_exists,
    get_file_size,
    get_files_by_extension,
    get_relative_path,
    read_json,
    read_lines,
    write_json,
)

# Logging utils module exports
from .logging_utils import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    ColoredFormatter,
    FormatString,
    FormatterProtocol,
    LogLevel,
    LogLevelName,
    LoggerName,
    get_logger,
    setup_logger,
)

__all__: list[str] = [
    # Submodules
    "colors",
    "file_utils",
    "logging_utils",
    # Colors - classes and types
    "Colors",
    "ColorScheme",
    "ColorCode",
    "AnsiCode",
    "FormattedText",
    # Colors - functions
    "colorize",
    "success",
    "warning",
    "error",
    "info",
    "bold",
    "header",
    "separator",
    # File utils - types and constants
    "StrPath",
    "JSONDict",
    "FileSize",
    "DEFAULT_ENCODING",
    "DEFAULT_JSON_INDENT",
    # File utils - functions
    "ensure_dir",
    "read_json",
    "write_json",
    "file_exists",
    "read_lines",
    "get_files_by_extension",
    "get_file_size",
    "get_relative_path",
    # Logging utils - types and constants
    "LogLevel",
    "LogLevelName",
    "FormatString",
    "LoggerName",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    # Logging utils - classes and functions
    "FormatterProtocol",
    "ColoredFormatter",
    "setup_logger",
    "get_logger",
]
