"""
Type definitions for Docker Compose Utils utilities.

This module contains all data models and type definitions used throughout
the docker-compose-utils package.
"""

from dataclasses import asdict, dataclass, field
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class InventoryRequest(BaseModel):
    """Request model for inventory endpoint."""

    src_path: str = Field(
        default="src",
        min_length=1,
        max_length=255,
        description="Source directory path"
    )

    @field_validator("src_path")
    @classmethod
    def validate_src_path(cls, v: str) -> str:
        """Validate source path for security."""
        from ..config.config import get_security_config

        security_config = get_security_config()
        if not security_config.input_validation_enabled:
            return v

        # Check against allowed patterns
        import fnmatch
        allowed = False
        for pattern in security_config.allowed_path_patterns:
            if fnmatch.fnmatch(v, pattern):
                allowed = True
                break

        if not allowed:
            raise ValueError(f"Path '{v}' is not in allowed patterns")

        # Prevent directory traversal
        if ".." in v or v.startswith("/"):
            raise ValueError("Invalid path: directory traversal not allowed")

        return v


class LinkCheckRequest(BaseModel):
    """Request model for link checking endpoint."""

    workers: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Number of concurrent workers"
    )
    timeout: int = Field(
        default=10,
        ge=1,
        le=300,
        description="Request timeout in seconds"
    )


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
