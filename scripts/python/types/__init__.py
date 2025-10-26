"""Type definitions package for Python scripts.

Centralized type aliases, enums, constants, and base classes.
Zero hardcoding - all values defined once and imported.

Subpackages:
    enums: Enumeration types for status, levels, categories
    constants: Configuration constants grouped by domain
    base: Base classes and protocols for common patterns

Examples:
    >>> from python.types.enums import CheckStatus, ConfigType
    >>> from python.types.constants import BLACK_LINE_LENGTH
    >>> from python.types.base import CheckerProtocol
    >>> from python.types.aliases import ErrorMessage, StrPath
"""

from . import (
    aliases,
    aliases_audit,
    aliases_colors,
    aliases_logging,
    aliases_mcp,
    aliases_validation,
    base,
    constants,
    enums,
)

__all__: list[str] = [
    "enums",
    "constants",
    "base",
    "aliases",
    "aliases_audit",
    "aliases_validation",
    "aliases_mcp",
    "aliases_colors",
    "aliases_logging",
]
