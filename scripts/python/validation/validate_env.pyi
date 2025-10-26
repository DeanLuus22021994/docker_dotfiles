"""Type stubs for validate_env module.

Provides type hints for environment variable validation utilities.
"""

from dataclasses import dataclass
from typing import Final, TypeAlias

# Type aliases
EnvVarName: TypeAlias = str
EnvVarValue: TypeAlias = str
Description: TypeAlias = str
ExitCode: TypeAlias = int

# Constants
MASK_LENGTH: Final[int]
MASK_SUFFIX: Final[str]
SHORT_MASK: Final[str]

@dataclass(frozen=True, slots=True)
class EnvVarConfig:
    """Configuration for an environment variable."""

    name: EnvVarName
    description: Description
    required: bool

    @property
    def is_set(self) -> bool: ...
    def get_masked_value(self) -> str: ...

@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Result of environment validation."""

    missing_required: tuple[EnvVarConfig, ...]
    missing_optional: tuple[EnvVarConfig, ...]
    present_vars: tuple[EnvVarConfig, ...]

    @property
    def is_valid(self) -> bool: ...
    @property
    def has_warnings(self) -> bool: ...
    @property
    def total_missing(self) -> int: ...

# Environment variable configurations
REQUIRED_ENV_VARS: Final[tuple[EnvVarConfig, ...]]
OPTIONAL_ENV_VARS: Final[tuple[EnvVarConfig, ...]]

class EnvValidator:
    """Validates environment variables configuration."""

    required_vars: tuple[EnvVarConfig, ...]
    optional_vars: tuple[EnvVarConfig, ...]
    verbose: bool

    def __init__(
        self,
        *,
        required_vars: tuple[EnvVarConfig, ...] = REQUIRED_ENV_VARS,
        optional_vars: tuple[EnvVarConfig, ...] = OPTIONAL_ENV_VARS,
        verbose: bool = True,
    ) -> None: ...
    def validate(self) -> ValidationResult: ...

class ValidationReporter:
    """Formats and displays validation results."""

    @staticmethod
    def print_summary(result: ValidationResult) -> None: ...

def main() -> ExitCode:
    """Run environment validation."""
    ...

# Backward-compatible wrapper functions
def validate_env_vars() -> tuple[bool, list[str], list[str]]:
    """Legacy wrapper: Validate environment variables."""
    ...

def print_summary(all_valid: bool, missing_required: list[str], missing_optional: list[str]) -> None:
    """Legacy wrapper: Print validation summary."""
    ...

__all__: list[str]
