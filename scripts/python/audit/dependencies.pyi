"""Type stubs for dependencies module.

Provides type hints for dependency checking utilities.
"""

import subprocess
from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Protocol, TypeAlias

# Type aliases
PackageName: TypeAlias = str
Version: TypeAlias = str
CommandArgs: TypeAlias = Sequence[str]
ErrorMessage: TypeAlias = str
ExitCode: TypeAlias = int

# Constants
REQUIRED_PACKAGES: Final[tuple[PackageName, ...]]
PYPROJECT_PATH: Final[Path]

@dataclass(frozen=True, slots=True)
class Package:
    """Python package with version information."""

    name: PackageName
    current_version: Version
    latest_version: Version | None

    @property
    def is_outdated(self) -> bool:
        """Check if package is outdated."""
    @property
    def version_info(self) -> str:
        """Get version information string."""

@dataclass(frozen=True, slots=True)
class DependencyCheckResult:
    """Result of a dependency check."""

    passed: bool
    check_name: str
    packages: tuple[Package, ...]
    missing_packages: tuple[PackageName, ...]
    errors: tuple[ErrorMessage, ...]
    warnings: tuple[str, ...]

    @property
    def has_issues(self) -> bool:
        """Check if any issues exist."""
    @property
    def outdated_packages(self) -> tuple[Package, ...]:
        """Get outdated packages."""

@dataclass(frozen=True, slots=True)
class DependencyReport:
    """Aggregated results from all dependency checks."""

    results: tuple[DependencyCheckResult, ...]

    @property
    def passed(self) -> bool:
        """Check if all checks passed."""
    @property
    def has_issues(self) -> bool:
        """Check if any issues exist."""
    @property
    def all_errors(self) -> tuple[ErrorMessage, ...]:
        """All error messages combined."""
    @property
    def all_warnings(self) -> tuple[str, ...]:
        """All warnings combined."""
    @property
    def all_outdated_packages(self) -> tuple[Package, ...]:
        """All outdated packages combined."""
    @property
    def all_missing_packages(self) -> tuple[PackageName, ...]:
        """All missing packages combined."""

class DependencyCheckerProtocol(Protocol):
    """Protocol for dependency checkers."""

    @property
    def check_name(self) -> str:
        """Name of the check."""
    def run(self) -> DependencyCheckResult:
        """Run the dependency check."""

class BaseDependencyChecker(ABC):
    """Abstract base class for dependency checkers."""

    verbose: bool

    @property
    def check_name(self) -> str:
        """Name of the check."""
    def run(self) -> DependencyCheckResult:
        """Run the dependency check."""
    def _run_pip_command(self, args: CommandArgs, /) -> subprocess.CompletedProcess[str]:
        """Run pip command with arguments."""

class OutdatedPackagesChecker(BaseDependencyChecker):
    """Checks for outdated Python packages."""

    @property
    def check_name(self) -> str:
        """Name of the check."""
    def run(self) -> DependencyCheckResult:
        """Run the outdated packages check."""
    def _parse_outdated_output(self, output: str, /) -> tuple[Package, ...]:
        """Parse outdated packages output."""

class InstalledPackagesChecker(BaseDependencyChecker):
    """Lists all installed packages."""

    @property
    def check_name(self) -> str:
        """Name of the check."""
    def run(self) -> DependencyCheckResult:
        """Run the installed packages check."""
    def _parse_installed_output(self, output: str, /) -> tuple[Package, ...]:
        """Parse installed packages output."""

class PyprojectDependenciesChecker(BaseDependencyChecker):
    """Checks pyproject.toml dependencies."""

    @property
    def check_name(self) -> str:
        """Name of the check."""
    def run(self) -> DependencyCheckResult:
        """Run the pyproject.toml dependencies check."""

class DependencyAuditor:
    """Orchestrates dependency checks."""

    verbose: bool
    checkers: tuple[BaseDependencyChecker, ...]

    def run_all_checks(self) -> DependencyReport:
        """Run all configured dependency checks."""
    def print_summary(self, report: DependencyReport, /) -> None:
        """Print summary of check results."""

def check_outdated_packages() -> tuple[bool, list[str]]:
    """Check for outdated packages."""

def list_installed_packages() -> tuple[bool, list[str]]:
    """List installed packages."""

def check_pyproject_dependencies() -> tuple[bool, list[str]]:
    """Check pyproject.toml dependencies."""

def main() -> ExitCode:
    """Run all dependency checks."""

__all__: list[str]
