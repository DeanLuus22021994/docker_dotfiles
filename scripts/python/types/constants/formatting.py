"""Formatting and display constants."""

from typing import Final

# Code formatting
BLACK_LINE_LENGTH: Final[int] = 100
RUFF_LINE_LENGTH: Final[int] = 100
YAML_LINE_LENGTH: Final[int] = 120

# JSON formatting
DEFAULT_JSON_INDENT: Final[int] = 2

# Masking constants for sensitive data display
MASK_LENGTH: Final[int] = 8
MASK_SUFFIX: Final[str] = "..."
SHORT_MASK: Final[str] = "***"

__all__: list[str] = [
    "BLACK_LINE_LENGTH",
    "RUFF_LINE_LENGTH",
    "YAML_LINE_LENGTH",
    "DEFAULT_JSON_INDENT",
    "MASK_LENGTH",
    "MASK_SUFFIX",
    "SHORT_MASK",
]
