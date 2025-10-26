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
    def is_outdated(self) -> bool: ...
    
    @property
    def version_info(self) -> str: ...

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
    def has_issues(self) -> bool: ...
    
    @property
    def outdated_packages(self) -> tuple[Package, ...]: ...

@dataclass(frozen=True, slots=True)
class DependencyReport:
    """Aggregated results from all dependency checks."""
    
    results: tuple[DependencyCheckResult, ...]
    
    @property
    def passed(self) -> bool: ...
    
    @property
    def has_issues(self) -> bool: ...
    
    @property
    def all_errors(self) -> tuple[ErrorMessage, ...]: ...
    
    @property
    def all_warnings(self) -> tuple[str, ...]: ...
    
    @property
    def all_outdated_packages(self) -> tuple[Package, ...]: ...
    
    @property
    def all_missing_packages(self) -> tuple[PackageName, ...]: ...

class DependencyCheckerProtocol(Protocol):
    """Protocol for dependency checkers."""
    
    @property
    def check_name(self) -> str: ...
    
    def run(self) -> DependencyCheckResult: ...

class BaseDependencyChecker(ABC):
    """Abstract base class for dependency checkers."""
    
    verbose: bool
    
    def __init__(self, *, verbose: bool = True) -> None: ...
    
    @property
    def check_name(self) -> str: ...
    
    def run(self) -> DependencyCheckResult: ...
    
    def _run_pip_command(self, args: CommandArgs) -> subprocess.CompletedProcess[str]: ...

class OutdatedPackagesChecker(BaseDependencyChecker):
    """Checks for outdated Python packages."""
    
    @property
    def check_name(self) -> str: ...
    
    def run(self) -> DependencyCheckResult: ...
    
    def _parse_outdated_output(self, output: str) -> tuple[Package, ...]: ...

class InstalledPackagesChecker(BaseDependencyChecker):
    """Lists all installed packages."""
    
    @property
    def check_name(self) -> str: ...
    
    def run(self) -> DependencyCheckResult: ...
    
    def _parse_installed_output(self, output: str) -> tuple[Package, ...]: ...

class PyprojectDependenciesChecker(BaseDependencyChecker):
    """Checks pyproject.toml dependencies."""
    
    @property
    def check_name(self) -> str: ...
    
    def run(self) -> DependencyCheckResult: ...

class DependencyAuditor:
    """Orchestrates dependency checks."""
    
    verbose: bool
    checkers: tuple[BaseDependencyChecker, ...]
    
    def __init__(self, *, verbose: bool = True) -> None: ...
    
    def run_all_checks(self) -> DependencyReport: ...
    
    def print_summary(self, report: DependencyReport) -> None: ...

def main() -> ExitCode:
    """Run all dependency checks."""
    ...

__all__: list[str]
