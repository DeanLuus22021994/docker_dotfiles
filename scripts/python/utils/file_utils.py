#!/usr/bin/env python3
"""
Shared File Utilities Module

Provides cross-platform file operation helpers with type-safe interfaces.
Handles JSON parsing, file I/O, directory operations, and path management
with proper error handling and encoding support.

Examples:
    >>> from python.utils.file_utils import read_json, ensure_dir
    >>> config = read_json('.config/settings.json')
    >>> ensure_dir('logs/')
"""

__all__: list[str] = [
    "read_json",
    "write_json",
    "read_lines",
    "file_exists",
    "ensure_dir",
    "get_files_by_extension",
    "get_file_size",
    "get_relative_path",
]

import json
import os
from pathlib import Path
from typing import Any, Optional


def read_json(file_path: str) -> dict[str, Any]:
    """
    Read and parse JSON file

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON as dictionary

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    with open(file_path, "r", encoding="utf-8") as f:
        result: dict[str, Any] = json.load(f)
        return result


def write_json(file_path: str, data: dict[str, Any], indent: int = 2) -> None:
    """
    Write dictionary to JSON file

    Args:
        file_path: Path to output JSON file
        data: Dictionary to write
        indent: JSON indentation (default: 2)
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)


def read_lines(file_path: str, strip: bool = True) -> list[str]:
    """
    Read file lines into list

    Args:
        file_path: Path to file
        strip: Strip whitespace from lines (default: True)

    Returns:
        List of lines
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if strip:
        return [line.strip() for line in lines]
    return lines


def file_exists(file_path: str) -> bool:
    """
    Check if file exists

    Args:
        file_path: Path to file

    Returns:
        True if file exists, False otherwise
    """
    return Path(file_path).exists()


def ensure_dir(dir_path: str) -> None:
    """
    Ensure directory exists, create if needed

    Args:
        dir_path: Path to directory
    """
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def get_files_by_extension(directory: str, extension: str, recursive: bool = True) -> list[Path]:
    """
    Get all files with specific extension in directory

    Args:
        directory: Directory to search
        extension: File extension (e.g., '.py', '.json')
        recursive: Search subdirectories (default: True)

    Returns:
        List of Path objects
    """
    path = Path(directory)

    if not extension.startswith("."):
        extension = f".{extension}"

    if recursive:
        return list(path.rglob(f"*{extension}"))
    return list(path.glob(f"*{extension}"))


def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes

    Args:
        file_path: Path to file

    Returns:
        File size in bytes
    """
    return Path(file_path).stat().st_size


def get_relative_path(file_path: str, base_path: Optional[str] = None) -> str:
    """
    Get relative path from base path

    Args:
        file_path: Path to file
        base_path: Base path (default: current working directory)

    Returns:
        Relative path string
    """
    if base_path is None:
        base_path = os.getcwd()

    return os.path.relpath(file_path, base_path)
