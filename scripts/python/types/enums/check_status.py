"""Check and validation status enumeration."""

from enum import StrEnum, auto


class CheckStatus(StrEnum):
    """Status of check or validation operations."""

    PASSED = auto()
    FAILED = auto()
    WARNING = auto()
    SKIPPED = auto()
    NOT_RUN = auto()


__all__: list[str] = ["CheckStatus"]
