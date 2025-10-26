"""Type stubs for file_utils module.

Provides type hints for file and directory utilities.
"""

import os
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Final, TypeAlias

# Type aliases
StrPath: TypeAlias = str | os.PathLike[str]
JSONValue: TypeAlias = dict[str, Any] | list[Any] | str | int | float | bool | None
JSONDict: TypeAlias = dict[str, JSONValue]
FileSize: TypeAlias = int

# Constants
DEFAULT_ENCODING: Final[str]
DEFAULT_JSON_INDENT: Final[int]

def ensure_directory(path: StrPath) -> Path:
    """Ensure directory exists, creating if necessary."""
    ...

def read_json(file_path: StrPath) -> JSONDict:
    """Read and parse JSON file."""
    ...

def write_json(
    file_path: StrPath,
    data: JSONDict,
    indent: int = DEFAULT_JSON_INDENT,
) -> None:
    """Write data to JSON file."""
    ...

def file_exists(path: StrPath) -> bool:
    """Check if file exists."""
    ...

def read_lines(file_path: StrPath, *, strip: bool = True) -> list[str]:
    """Read file lines into list."""
    ...

def write_lines(file_path: StrPath, lines: Sequence[str]) -> None:
    """Write lines to file."""
    ...

def get_files_by_extension(
    directory: StrPath,
    extension: str,
    *,
    recursive: bool = False,
) -> Sequence[Path]:
    """Get files matching extension."""
    ...

def get_file_size(file_path: StrPath) -> FileSize:
    """Get file size in bytes."""
    ...

def safe_delete(file_path: StrPath) -> bool:
    """Safely delete file if it exists."""
    ...

__all__: list[str]
