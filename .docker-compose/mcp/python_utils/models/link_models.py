#!/usr/bin/env python3
"""
Data models for documentation utilities.

Enhanced for Python 3.14 with improved type safety.
"""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class LinkResult:
    """Result of a link check operation."""

    url: str
    is_valid: bool
    status_code: int | None = None
    error_message: str | None = None
    response_time: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ComponentInfo:
    """Information about a React component."""

    name: str
    file: str
    path: str
    category: str
    exports: list[str]
    imports: list[str]
    size_bytes: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)