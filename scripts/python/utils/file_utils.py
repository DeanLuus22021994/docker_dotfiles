#!/usr/bin/env python3
"""
Shared File Utilities Module

Provides cross-platform file operation helpers with type-safe interfaces.
Handles JSON parsing, file I/O, directory operations, and path management
with proper error handling and encoding support.

This module uses Python 3.14 type system features including TypeAlias, 
os.PathLike support, and recursive type definitions for improved type safety.

Examples:
    >>> from python.utils.file_utils import read_json, ensure_dir
    >>> config = read_json('.config/settings.json')
    >>> ensure_dir('logs/')
"""

import json
import os
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Final, TypeAlias

# Type aliases for semantic clarity and type safety
StrPath: TypeAlias = str | os.PathLike[str]
JSONValue: TypeAlias = dict[str, Any] | list[Any] | str | int | float | bool | None
JSONDict: TypeAlias = dict[str, JSONValue]
FileSize: TypeAlias = int

# Constants
DEFAULT_ENCODING: Final[str] = "utf-8"
DEFAULT_JSON_INDENT: Final[int] = 2

__all__: list[str] = [
    "read_json",
    "write_json",
    "read_lines",
    "file_exists",
    "ensure_dir",
    "get_files_by_extension",
    "get_file_size",
    "get_relative_path",
    "StrPath",
    "JSONDict",
    "FileSize",
]


def read_json(file_path: StrPath) -> JSONDict:
    """Read and parse JSON file.

    Args:
        file_path: Path to JSON file (str or PathLike)

    Returns:
        Parsed JSON as dictionary

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
        PermissionError: If file is not readable

    Example:
        >>> config = read_json(Path(".config/app.json"))
        >>> print(config["version"])
    """
    with open(file_path, "r", encoding=DEFAULT_ENCODING) as f:
        result: JSONDict = json.load(f)
        return result


def write_json(
    file_path: StrPath, data: JSONDict, indent: int = DEFAULT_JSON_INDENT
) -> None:
    """Write dictionary to JSON file.

    Args:
        file_path: Path to output JSON file (str or PathLike)
        data: Dictionary to write
        indent: JSON indentation spaces (default: 2)

    Raises:
        PermissionError: If file is not writable
        OSError: If disk is full or other I/O error

    Example:
        >>> config = {"version": "1.0", "debug": True}
        >>> write_json("config.json", config, indent=4)
    """
    with open(file_path, "w", encoding=DEFAULT_ENCODING) as f:
        json.dump(data, f, indent=indent)


def read_lines(file_path: StrPath, *, strip: bool = True) -> list[str]:
    """Read file lines into list.

    Args:
        file_path: Path to file (str or PathLike)
        strip: Strip whitespace from lines (default: True)

    Returns:
        List of lines from file

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file is not readable

    Example:
        >>> lines = read_lines("requirements.txt", strip=True)
        >>> packages = [line for line in lines if line and not line.startswith("#")]
    """
    with open(file_path, "r", encoding=DEFAULT_ENCODING) as f:
        lines = f.readlines()

    if strip:
        return [line.strip() for line in lines]
    return lines


def file_exists(file_path: StrPath) -> bool:
    """Check if file or directory exists.

    Args:
        file_path: Path to check (str or PathLike)

    Returns:
        True if path exists, False otherwise

    Example:
        >>> if file_exists(".env"):
        ...     print("Environment file found")
    """
    return Path(file_path).exists()


def ensure_dir(dir_path: StrPath) -> None:
    """Ensure directory exists, create if needed.

    Creates all parent directories as needed (like mkdir -p).

    Args:
        dir_path: Path to directory (str or PathLike)

    Raises:
        PermissionError: If directory cannot be created
        OSError: If creation fails for other reasons

    Example:
        >>> ensure_dir("logs/application/debug")
        >>> # All parent directories created if needed
    """
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def get_files_by_extension(
    directory: StrPath, extension: str, *, recursive: bool = True
) -> Sequence[Path]:
    """Get all files with specific extension in directory.

    Args:
        directory: Directory to search (str or PathLike)
        extension: File extension (e.g., '.py', '.json', or 'py')
        recursive: Search subdirectories recursively (default: True)

    Returns:
        Sequence of Path objects matching extension

    Example:
        >>> py_files = get_files_by_extension("src", ".py", recursive=True)
        >>> for file in py_files:
        ...     print(file.name)
    """
    path = Path(directory)

    if not extension.startswith("."):
        extension = f".{extension}"

    if recursive:
        return tuple(path.rglob(f"*{extension}"))
    return tuple(path.glob(f"*{extension}"))


def get_file_size(file_path: StrPath) -> FileSize:
    """Get file size in bytes.

    Args:
        file_path: Path to file (str or PathLike)

    Returns:
        File size in bytes

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file stats cannot be read

    Example:
        >>> size_bytes = get_file_size("large_file.bin")
        >>> size_mb = size_bytes / (1024 * 1024)
        >>> print(f"Size: {size_mb:.2f} MB")
    """
    return Path(file_path).stat().st_size


def get_relative_path(file_path: StrPath, base_path: StrPath | None = None) -> str:
    """Get relative path from base path.

    Args:
        file_path: Path to file (str or PathLike)
        base_path: Base path for relativity (default: current working directory)

    Returns:
        Relative path string

    Example:
        >>> rel_path = get_relative_path("/home/user/project/src/main.py", "/home/user")
        >>> print(rel_path)  # "project/src/main.py"
    """
    if base_path is None:
        base_path = os.getcwd()

    return os.path.relpath(file_path, base_path)
