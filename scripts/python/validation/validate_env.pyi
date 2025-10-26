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
    def is_set(self) -> bool:
        """Check if environment variable is set."""
    def get_masked_value(self) -> str:
        """Get masked value for display."""

@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Result of environment validation."""

    missing_required: tuple[EnvVarConfig, ...]
    missing_optional: tuple[EnvVarConfig, ...]
    present_vars: tuple[EnvVarConfig, ...]

    @property
    def is_valid(self) -> bool:
        """Check if all required variables are present."""
    @property
    def has_warnings(self) -> bool:
        """Check if any optional variables are missing."""
    @property
    def total_missing(self) -> int:
        """Total number of missing variables."""

# Environment variable configurations
REQUIRED_ENV_VARS: Final[tuple[EnvVarConfig, ...]]
OPTIONAL_ENV_VARS: Final[tuple[EnvVarConfig, ...]]

class EnvValidator:
    """Validates environment variables configuration."""

    required_vars: tuple[EnvVarConfig, ...]
    optional_vars: tuple[EnvVarConfig, ...]
    verbose: bool

    def validate(self) -> ValidationResult:
        """Validate environment variables."""

class ValidationReporter:
    """Formats and displays validation results."""

    @staticmethod
    def print_summary(result: ValidationResult, /) -> None:
        """Print formatted validation summary."""

def validate_env_vars() -> tuple[bool, list[str], list[str]]:
    """Validate environment variables.
    
    Returns:
        Tuple of (all_valid, missing_required, missing_optional)
    """

def print_summary(
    missing_required: list[str],
    missing_optional: list[str],
    /,
) -> None:
    """Print validation summary."""
    pass

def main() -> ExitCode:
    """Run environment validation."""

__all__: list[str]
