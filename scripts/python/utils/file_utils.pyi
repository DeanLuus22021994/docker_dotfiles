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

def ensure_directory(_path: StrPath, /) -> Path:
    """Ensure directory exists, creating if necessary."""
    ...

def ensure_dir(_dir_path: StrPath, /) -> None:
    """Ensure directory exists, creating if necessary (alias for compatibility)."""
    ...

def get_relative_path(_file_path: StrPath, _base_path: StrPath | None = None, /) -> str:
    """Get relative path from base to file."""
    ...

def read_json(_file_path: StrPath, /) -> JSONDict:
    """Read and parse JSON file."""
    ...

def write_json(
    _file_path: StrPath,
    _data: JSONDict,
    /,
    indent: int = 2,
) -> None:
    """Write data to JSON file."""
    ...

def file_exists(_path: StrPath, /) -> bool:
    """Check if file exists."""
    ...

def read_lines(_file_path: StrPath, /, *, strip: bool = True) -> list[str]:
    """Read file lines into list."""
    ...

def write_lines(_file_path: StrPath, _lines: Sequence[str], /) -> None:
    """Write lines to file."""
    ...

def get_files_by_extension(
    _directory: StrPath,
    _extension: str,
    /,
    *,
    recursive: bool = True,
) -> Sequence[Path]:
    """Get files matching extension."""
    ...

def get_file_size(_file_path: StrPath, /) -> FileSize:
    """Get file size in bytes."""
    ...

def safe_delete(_file_path: StrPath, /) -> bool:
    """Safely delete file if it exists."""
    ...

__all__: list[str]
