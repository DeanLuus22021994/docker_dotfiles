"""Common type aliases used across the package."""

import os
from collections.abc import Sequence
from pathlib import Path
from typing import Any, TypeAlias

# String-like types
ErrorMessage: TypeAlias = str
WarningMessage: TypeAlias = str
Description: TypeAlias = str
FieldName: TypeAlias = str

# Path types
StrPath: TypeAlias = str | os.PathLike[str]
ConfigPath: TypeAlias = Path

# Numeric types
ExitCode: TypeAlias = int
FileSize: TypeAlias = int
TokenCount: TypeAlias = int
ToolCount: TypeAlias = int

# Collection types
CommandArgs: TypeAlias = Sequence[str]
StrSequence: TypeAlias = Sequence[str]

# JSON types
JSONValue: TypeAlias = dict[str, Any] | list[Any] | str | int | float | bool | None
JSONDict: TypeAlias = dict[str, JSONValue]

__all__: list[str] = [
    "ErrorMessage",
    "WarningMessage",
    "Description",
    "FieldName",
    "StrPath",
    "ConfigPath",
    "ExitCode",
    "FileSize",
    "TokenCount",
    "ToolCount",
    "CommandArgs",
    "StrSequence",
    "JSONValue",
    "JSONDict",
]
