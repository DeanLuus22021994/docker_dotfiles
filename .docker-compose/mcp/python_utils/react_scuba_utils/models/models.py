"""
Type definitions for React Scuba utilities.

This module contains all data models and type definitions used throughout
the react-scuba-utils package.
"""

from dataclasses import asdict, dataclass, field
from typing import Any, Optional


@dataclass
class LinkResult:
    """
    Result of a link check operation.

    Attributes:
        url: The URL that was checked
        is_valid: Whether the link is accessible
        status_code: HTTP status code (if available)
        error_message: Error message (if any)
        response_time: Time taken for the request in seconds
    """

    url: str
    is_valid: bool
    status_code: int | None = None
    error_message: str | None = None
    response_time: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)


@dataclass
class ComponentInfo:
    """
    Information about a React component.

    Attributes:
        name: Component name
        file: Relative file path
        path: Absolute file path
        category: Component category (pages, components, hooks, utils)
        exports: List of exported symbols
        imports: List of imported modules
        size_bytes: File size in bytes
    """

    name: str
    file: str
    path: str
    category: str
    exports: list[str]
    imports: list[str]
    size_bytes: int

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)


@dataclass
class LinkCheckConfig:
    """
    Configuration for link checking operations.

    Attributes:
        max_workers: Maximum number of concurrent workers
        timeout: Request timeout in seconds
        retry_attempts: Number of retry attempts
        use_interpreters: Whether to use concurrent interpreters
        skip_domains: Domains to skip during checking
    """

    max_workers: int = 10
    timeout: int = 10
    retry_attempts: int = 3
    use_interpreters: bool = True
    skip_domains: list[str] = field(
        default_factory=lambda: ["localhost", "127.0.0.1", "0.0.0.0"]
    )


@dataclass
class ComponentInventoryConfig:
    """
    Configuration for component inventory generation.

    Attributes:
        src_path: Source directory path
        extensions: File extensions to scan
        categories: Component categories to include
    """

    src_path: str = "src"
    extensions: list[str] = field(
        default_factory=lambda: ["*.jsx", "*.js", "*.tsx", "*.ts"]
    )
    categories: list[str] = field(
        default_factory=lambda: ["pages", "components", "hooks", "utils"]
    )
