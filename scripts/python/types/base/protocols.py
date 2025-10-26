"""Base protocol definitions for checker interfaces."""

from collections.abc import Sequence
from typing import Protocol

from python.types.aliases import ErrorMessage


class CheckerProtocol(Protocol):
    """Common protocol for all checker types."""

    def run(self) -> tuple[bool, tuple[ErrorMessage, ...]]:
        """Execute the check and return (passed, errors)."""
        raise NotImplementedError


class ValidatorProtocol(Protocol):
    """Common protocol for all validator types."""

    def validate(self) -> tuple[bool, tuple[ErrorMessage, ...]]:
        """Execute validation and return (valid, errors)."""
        raise NotImplementedError


class CommandRunnerProtocol(Protocol):
    """Protocol for components that run external commands."""

    def run_command(self, args: Sequence[str]) -> tuple[int, str, str]:
        """Run command and return (exit_code, stdout, stderr)."""
        raise NotImplementedError


__all__: list[str] = ["CheckerProtocol", "ValidatorProtocol", "CommandRunnerProtocol"]
