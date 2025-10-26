#!/usr/bin/env python3
"""
Environment Variables Validation Script

Validates required and optional environment variables before stack startup.
Uses a modular validator architecture with dataclasses for configuration.

This module uses Python 3.14 type system features including dataclasses,
TypeAlias, Protocol, and Final for improved type safety.

Exit code: 0=success, 1=failure

Examples:
    >>> from validation.validate_env import EnvValidator
    >>> validator = EnvValidator()
    >>> report = validator.validate()
    >>> print(report.is_valid)  # True if all required vars set
"""

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, TypeAlias

# Add parent directory to path for imports
_script_dir = Path(__file__).parent.parent.parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

from scripts.python.utils.colors import (
    Colors,
    bold,
    error,
    header,
    separator,
    success,
    warning,
)

# Type aliases for semantic clarity
EnvVarName: TypeAlias = str
EnvVarValue: TypeAlias = str
Description: TypeAlias = str
ExitCode: TypeAlias = int

# Constants
MASK_LENGTH: Final[int] = 8
MASK_SUFFIX: Final[str] = "..."
SHORT_MASK: Final[str] = "***"


SHORT_MASK: Final[str] = "***"


@dataclass(frozen=True, slots=True)
class EnvVarConfig:
    """Configuration for an environment variable.

    Attributes:
        name: Environment variable name
        description: Human-readable description
        required: Whether variable is required (vs optional)
    """

    name: EnvVarName
    description: Description
    required: bool = True

    @property
    def is_set(self) -> bool:
        """Check if environment variable is currently set."""
        return os.getenv(self.name) is not None

    def get_masked_value(self) -> str:
        """Get masked value for display.

        Returns:
            Masked value string, or empty if not set
        """
        value = os.getenv(self.name)
        if not value:
            return ""

        if len(value) > MASK_LENGTH:
            return f"{value[:MASK_LENGTH]}{MASK_SUFFIX}"
        return SHORT_MASK


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Result of environment validation.

    Attributes:
        missing_required: Required variables that are not set
        missing_optional: Optional variables that are not set
        present_vars: Variables that are properly set
    """

    missing_required: tuple[EnvVarConfig, ...] = field(default_factory=tuple)
    missing_optional: tuple[EnvVarConfig, ...] = field(default_factory=tuple)
    present_vars: tuple[EnvVarConfig, ...] = field(default_factory=tuple)

    @property
    def is_valid(self) -> bool:
        """Check if all required variables are set."""
        return len(self.missing_required) == 0

    @property
    def has_warnings(self) -> bool:
        """Check if any optional variables are missing."""
        return len(self.missing_optional) > 0

    @property
    def total_missing(self) -> int:
        """Total count of missing variables."""
        return len(self.missing_required) + len(self.missing_optional)


# Environment variable configurations
REQUIRED_ENV_VARS: Final[tuple[EnvVarConfig, ...]] = (
    EnvVarConfig("GITHUB_OWNER", "GitHub organization/username for API access", required=True),
    EnvVarConfig("GH_PAT", "GitHub Personal Access Token for authentication", required=True),
    EnvVarConfig("DOCKER_POSTGRES_PASSWORD", "PostgreSQL database password", required=True),
    EnvVarConfig("DOCKER_MARIADB_ROOT_PASSWORD", "MariaDB root password", required=True),
    EnvVarConfig("DOCKER_MARIADB_PASSWORD", "MariaDB cluster_user password", required=True),
    EnvVarConfig("DOCKER_REDIS_PASSWORD", "Redis authentication password", required=True),
    EnvVarConfig("DOCKER_MINIO_ROOT_USER", "MinIO root username", required=True),
    EnvVarConfig("DOCKER_MINIO_ROOT_PASSWORD", "MinIO root password", required=True),
    EnvVarConfig("DOCKER_GRAFANA_ADMIN_PASSWORD", "Grafana admin password", required=True),
    EnvVarConfig("DOCKER_JUPYTER_TOKEN", "Jupyter notebook access token", required=True),
    EnvVarConfig("DOCKER_PGADMIN_PASSWORD", "pgAdmin web interface password", required=True),
)

OPTIONAL_ENV_VARS: Final[tuple[EnvVarConfig, ...]] = (
    EnvVarConfig(
        "DOCKER_ACCESS_TOKEN",
        "Docker Hub access token for increased pull limits",
        required=False,
    ),
    EnvVarConfig("CODECOV_TOKEN", "Codecov token for coverage reporting", required=False),
)


class EnvValidator:
    """Validates environment variables configuration.

    Checks required and optional environment variables,
    providing detailed status and instructions.

    Example:
        >>> validator = EnvValidator()
        >>> result = validator.validate()
        >>> if result.is_valid:
        ...     print("Ready to start!")
    """

    def __init__(
        self,
        *,
        required_vars: tuple[EnvVarConfig, ...] = REQUIRED_ENV_VARS,
        optional_vars: tuple[EnvVarConfig, ...] = OPTIONAL_ENV_VARS,
        verbose: bool = True,
    ) -> None:
        """Initialize validator.

        Args:
            required_vars: Required environment variables config
            optional_vars: Optional environment variables config
            verbose: Enable verbose output (default: True)
        """
        self.required_vars = required_vars
        self.optional_vars = optional_vars
        self.verbose = verbose

    def validate(self) -> ValidationResult:
        """Validate all environment variables.

        Returns:
            ValidationResult with missing/present variables
        """
        if self.verbose:
            print(f"\n{header('=== Environment Variables Validation ===')}\n")

        missing_required: list[EnvVarConfig] = []
        missing_optional: list[EnvVarConfig] = []
        present_vars: list[EnvVarConfig] = []

        # Check required variables
        if self.verbose:
            print(f"{bold('Required Variables:')}")

        for var_config in self.required_vars:
            if var_config.is_set:
                present_vars.append(var_config)
                if self.verbose:
                    masked = var_config.get_masked_value()
                    print(f"  {success(f'{var_config.name}: {masked}')}")
            else:
                missing_required.append(var_config)
                if self.verbose:
                    print(f"  {error(f'{var_config.name}: NOT SET - {var_config.description}')}")

        # Check optional variables
        if self.verbose:
            print(f"\n{bold('Optional Variables:')}")

        for var_config in self.optional_vars:
            if var_config.is_set:
                present_vars.append(var_config)
                if self.verbose:
                    masked = var_config.get_masked_value()
                    print(f"  {success(f'{var_config.name}: {masked}')}")
            else:
                missing_optional.append(var_config)
                if self.verbose:
                    print(f"  {warning(f'{var_config.name}: NOT SET - {var_config.description}')}")

        return ValidationResult(
            missing_required=tuple(missing_required),
            missing_optional=tuple(missing_optional),
            present_vars=tuple(present_vars),
        )


class ValidationReporter:
    """Formats and displays validation results.

    Provides human-readable output with actionable instructions
    for fixing missing environment variables.
    """

    @staticmethod
    def print_summary(result: ValidationResult) -> None:
        """Print validation summary with instructions.

        Args:
            result: Validation result to display
        """
        print(f"\n{separator()}")

        if result.is_valid:
            print(f"{success('All required environment variables are set!')}")

            if result.has_warnings:
                print(f"\n{warning('Optional variables missing:')}")
                for var in result.missing_optional:
                    print(f"  - {var.name}")
                print(f"\n{warning('Consider setting these for full functionality.')}")

            print(f"\n{Colors.GREEN}You can now start the stack:{Colors.RESET}")
            print("  docker-compose up -d")
            print("  docker-compose --profile dev up -d  # Include devcontainer")

        else:
            print(f"{error('Missing required environment variables!')}")
            print(f"\n{Colors.RED}Required variables missing:{Colors.RESET}")
            for var in result.missing_required:
                print(f"  - {var.name}: {var.description}")

            print(f"\n{Colors.BLUE}To fix this:{Colors.RESET}")
            print("  1. Copy .env.example to .env:")
            print("     cp .env.example .env")
            print("  2. Edit .env and fill in your values")
            print("  3. Source the .env file:")
            print("     export $(cat .env | xargs)  # Linux/macOS")
            powershell_cmd = (
                "     Get-Content .env | ForEach-Object { $var = $_.Split('='); "
                "[Environment]::SetEnvironmentVariable($var[0], $var[1], 'Process') }  # PowerShell"
            )
            print(powershell_cmd)
            print("  4. Run this script again to verify")

        print(f"{separator()}\n")


def main() -> ExitCode:
    """Run environment validation and return exit code.

    Returns:
        0 if all required vars set, 1 otherwise
    """
    validator = EnvValidator()
    result = validator.validate()

    reporter = ValidationReporter()
    reporter.print_summary(result)

    return 0 if result.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
