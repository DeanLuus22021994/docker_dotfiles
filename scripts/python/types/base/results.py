"""Base result classes for common patterns across modules."""

from dataclasses import dataclass, field

from python.types.aliases import ErrorMessage


@dataclass(frozen=True, slots=True)
class BaseResult:
    """Base result class with common success/failure pattern.

    All result types inherit this to eliminate duplicate code.
    """

    passed: bool
    errors: tuple[ErrorMessage, ...] = field(default_factory=tuple)

    @property
    def failed(self) -> bool:
        """Convenience property - inverse of passed."""
        return not self.passed

    @property
    def has_errors(self) -> bool:
        """Check if any errors exist."""
        return len(self.errors) > 0


__all__: list[str] = ["BaseResult"]
