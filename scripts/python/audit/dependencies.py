#!/usr/bin/env python3
"""
Dependencies Audit Script

Checks for outdated packages, missing dependencies, and displays current
versions using a modular checker architecture. Each check type is wrapped
in a dedicated class following the Single Responsibility Principle.

This module uses Python 3.14 type system features including dataclasses,
TypeAlias, Protocol, and Final for improved type safety.

Exit code: 0=success, 1=warning

Examples:
    >>> from audit.dependencies import DependencyAuditor
    >>> auditor = DependencyAuditor()
    >>> report = auditor.run_all_checks()
    >>> print(report.has_issues)  # True if issues found
"""

import subprocess
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol

from python.types.aliases import CommandArgs, ErrorMessage, ExitCode
from python.types.aliases_audit import PackageName, Version
from python.types.constants import PYPROJECT_PATH, REQUIRED_PACKAGES
from python.utils.colors import error, header, info, separator, success, warning


@dataclass(frozen=True, slots=True)
class Package:
    """Represents a Python package with version information.

    Attributes:
        name: Package name (normalized to lowercase)
        current_version: Currently installed version
        latest_version: Latest available version (None if unknown)
    """

    name: PackageName
    current_version: Version
    latest_version: Version | None = None

    @property
    def is_outdated(self) -> bool:
        """Check if package has newer version available."""
        return self.latest_version is not None and self.current_version != self.latest_version

    @property
    def version_info(self) -> str:
        """Human-readable version information."""
        if self.is_outdated:
            return f"{self.name}: {self.current_version} -> {self.latest_version}"
        return f"{self.name}: {self.current_version}"


@dataclass(frozen=True, slots=True)
class DependencyCheckResult:
    """Result of a dependency check.

    Attributes:
        passed: Whether the check succeeded without issues
        check_name: Name of the check that ran
        packages: Packages found during check (if applicable)
        missing_packages: Package names that are missing
        errors: List of error messages
        warnings: List of warning messages
    """

    passed: bool
    check_name: str
    packages: tuple[Package, ...] = field(default_factory=tuple)
    missing_packages: tuple[PackageName, ...] = field(default_factory=tuple)
    errors: tuple[ErrorMessage, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)

    @property
    def has_issues(self) -> bool:
        """Check if result contains errors or warnings."""
        return len(self.errors) > 0 or len(self.warnings) > 0

    @property
    def outdated_packages(self) -> tuple[Package, ...]:
        """Get only outdated packages."""
        return tuple(pkg for pkg in self.packages if pkg.is_outdated)


@dataclass(frozen=True, slots=True)
class DependencyReport:
    """Aggregated results from all dependency checks.

    Attributes:
        results: Tuple of all check results
    """

    results: tuple[DependencyCheckResult, ...]

    @property
    def passed(self) -> bool:
        """Check if all dependency checks passed."""
        return all(result.passed for result in self.results)

    @property
    def has_issues(self) -> bool:
        """Check if any issues were found."""
        return any(result.has_issues for result in self.results)

    @property
    def all_errors(self) -> tuple[ErrorMessage, ...]:
        """Collect all errors from checks."""
        errors: list[ErrorMessage] = []
        for result in self.results:
            errors.extend(result.errors)
        return tuple(errors)

    @property
    def all_warnings(self) -> tuple[str, ...]:
        """Collect all warnings from checks."""
        warnings: list[str] = []
        for result in self.results:
            warnings.extend(result.warnings)
        return tuple(warnings)

    @property
    def all_outdated_packages(self) -> tuple[Package, ...]:
        """Get all outdated packages from all checks."""
        packages: list[Package] = []
        for result in self.results:
            packages.extend(result.outdated_packages)
        return tuple(packages)

    @property
    def all_missing_packages(self) -> tuple[PackageName, ...]:
        """Get all missing packages from all checks."""
        missing: list[PackageName] = []
        for result in self.results:
            missing.extend(result.missing_packages)
        return tuple(missing)


class DependencyCheckerProtocol(Protocol):
    """Protocol defining interface for dependency checkers."""

    @property
    def check_name(self) -> str:
        """Name of the dependency check."""
        raise NotImplementedError

    def run(self) -> DependencyCheckResult:
        """Run the dependency check.

        Returns:
            DependencyCheckResult with packages and issues
        """
        raise NotImplementedError


class BaseDependencyChecker(ABC):
    """Abstract base class for dependency checkers."""

    def __init__(self, *, verbose: bool = True) -> None:
        """Initialize checker.

        Args:
            verbose: Enable verbose output (default: True)
        """
        self.verbose = verbose

    @property
    @abstractmethod
    def check_name(self) -> str:
        """Name of the dependency check."""
        raise NotImplementedError

    @abstractmethod
    def run(self) -> DependencyCheckResult:
        """Run the dependency check."""
        raise NotImplementedError

    def _run_pip_command(self, args: CommandArgs) -> subprocess.CompletedProcess[str]:
        """Run pip command with given arguments.

        Args:
            args: Command arguments after 'pip'

        Returns:
            Completed subprocess result

        Raises:
            FileNotFoundError: If pip is not available
        """
        return subprocess.run(
            [sys.executable, "-m", "pip", *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def _handle_pip_not_found(self) -> DependencyCheckResult:
        """Handle FileNotFoundError for missing pip command.

        Returns:
            DependencyCheckResult indicating pip not found
        """
        error_msg = "pip not found. Ensure Python environment is activated."
        if self.verbose:
            print(error(error_msg))
        return DependencyCheckResult(
            passed=False,
            check_name=self.check_name,
            errors=(error_msg,),
        )

    def _parse_pip_list_output(
        self, output: str, *, include_latest: bool = False
    ) -> tuple[Package, ...]:
        """Parse pip list output into Package objects.

        Args:
            output: Raw pip list output
            include_latest: Whether output includes latest version column

        Returns:
            Tuple of Package objects
        """
        packages: list[Package] = []
        lines = output.strip().split("\n")[2:]  # Skip header lines

        for line in lines:
            parts = line.split()
            if include_latest and len(parts) >= 3:
                name, current, latest = parts[0], parts[1], parts[2]
                packages.append(
                    Package(name=name, current_version=current, latest_version=latest)
                )
            elif not include_latest and len(parts) >= 2:
                name, version = parts[0], parts[1]
                packages.append(Package(name=name, current_version=version))

        return tuple(packages)


class OutdatedPackagesChecker(BaseDependencyChecker):
    """Checks for outdated Python packages."""

    @property
    def check_name(self) -> str:
        return "Outdated Packages"

    def run(self) -> DependencyCheckResult:
        """Check for outdated packages."""
        if self.verbose:
            print(f"\n{header('=== Checking Outdated Packages ===')}")

        try:
            result = self._run_pip_command(["list", "--outdated"])

            if result.stdout.strip():
                # Parse outdated packages
                packages = self._parse_pip_list_output(result.stdout, include_latest=True)
                warnings_msg = (f"Found {len(packages)} outdated package(s)",)

                if self.verbose:
                    print(warning("Outdated packages found"))
                    print(result.stdout)
                    print(info("Run 'pip install --upgrade <package>' to update"))

                return DependencyCheckResult(
                    passed=False,
                    check_name=self.check_name,
                    packages=packages,
                    warnings=warnings_msg,
                )

            if self.verbose:
                print(success("All packages are up to date"))
            return DependencyCheckResult(passed=True, check_name=self.check_name)

        except FileNotFoundError:
            return self._handle_pip_not_found()


class InstalledPackagesChecker(BaseDependencyChecker):
    """Lists all installed packages and versions."""

    @property
    def check_name(self) -> str:
        return "Installed Packages"

    def run(self) -> DependencyCheckResult:
        """List all installed packages."""
        if self.verbose:
            print(f"\n{header('=== Installed Packages ===')}")

        try:
            result = self._run_pip_command(["list"])

            if self.verbose:
                print(result.stdout)
                print(success("Package list retrieved successfully"))

            packages = self._parse_pip_list_output(result.stdout, include_latest=False)
            return DependencyCheckResult(
                passed=True,
                check_name=self.check_name,
                packages=packages,
            )

        except FileNotFoundError:
            return self._handle_pip_not_found()


class PyprojectDependenciesChecker(BaseDependencyChecker):
    """Checks if all pyproject.toml dependencies are installed."""

    @property
    def check_name(self) -> str:
        return "Required Dependencies"

    def run(self) -> DependencyCheckResult:
        """Check if required dependencies from pyproject.toml are installed."""
        if self.verbose:
            print(f"\n{header('=== Checking pyproject.toml Dependencies ===')}")

        if not PYPROJECT_PATH.exists():
            if self.verbose:
                print(info("No pyproject.toml found"))
            return DependencyCheckResult(passed=True, check_name=self.check_name)

        try:
            result = self._run_pip_command(["list"])
            installed = result.stdout.lower()

            missing = tuple(pkg for pkg in REQUIRED_PACKAGES if pkg.lower() not in installed)

            if missing:
                error_msg = f"Missing packages: {', '.join(missing)}"
                if self.verbose:
                    print(warning(f"Missing required packages: {', '.join(missing)}"))
                    print(info(f"Run 'pip install {' '.join(missing)}' to install"))

                return DependencyCheckResult(
                    passed=False,
                    check_name=self.check_name,
                    missing_packages=missing,
                    errors=(error_msg,),
                )

            if self.verbose:
                print(success("All required dependencies installed"))
            return DependencyCheckResult(passed=True, check_name=self.check_name)

        except FileNotFoundError:
            return self._handle_pip_not_found()


class DependencyAuditor:
    """Orchestrates dependency checks across multiple checkers.

    Runs checks for required, outdated, and installed packages,
    aggregating results into a comprehensive report.

    Example:
        >>> auditor = DependencyAuditor()
        >>> report = auditor.run_all_checks()
        >>> if report.passed:
        ...     print("All dependencies OK!")
    """

    def __init__(self, *, verbose: bool = True) -> None:
        """Initialize auditor with checkers.

        Args:
            verbose: Enable verbose output (default: True)
        """
        self.verbose = verbose
        self.checkers: tuple[BaseDependencyChecker, ...] = (
            PyprojectDependenciesChecker(verbose=verbose),
            OutdatedPackagesChecker(verbose=verbose),
            InstalledPackagesChecker(verbose=verbose),
        )

    def run_all_checks(self) -> DependencyReport:
        """Run all configured dependency checks.

        Returns:
            DependencyReport with aggregated results
        """
        if self.verbose:
            print(separator())
            print(header("Dependencies Audit"))
            print(separator())

        results: list[DependencyCheckResult] = []
        for checker in self.checkers:
            result = checker.run()
            results.append(result)

        return DependencyReport(results=tuple(results))

    def print_summary(self, report: DependencyReport) -> None:
        """Print human-readable summary of audit results.

        Args:
            report: Report to summarize
        """
        print(f"\n{separator()}")
        if report.passed:
            print(success("ALL DEPENDENCY CHECKS PASSED"))
        else:
            issue_count = len(report.all_errors) + len(report.all_warnings)
            print(warning(f"DEPENDENCY AUDIT COMPLETED WITH WARNINGS ({issue_count} issue(s))"))

        print(separator())

        if report.has_issues:
            if report.all_errors:
                print("\nErrors:")
                for err in report.all_errors:
                    print(f"  - {err}")

            if report.all_warnings:
                print("\nWarnings:")
                for warn in report.all_warnings:
                    print(f"  - {warn}")


def main() -> ExitCode:
    """Run all dependency checks and return exit code.

    Returns:
        0 if all checks passed, 1 if warnings/errors found
    """
    auditor = DependencyAuditor()
    report = auditor.run_all_checks()
    auditor.print_summary(report)

    return 0 if report.passed else 1


# Backward-compatible wrapper functions for legacy test code
def check_outdated_packages() -> tuple[bool, list[str]]:
    """Legacy wrapper: Check for outdated packages.

    Returns:
        Tuple of (passed, errors) for backward compatibility
    """
    checker = OutdatedPackagesChecker(verbose=False)
    result = checker.run()
    errors = list(result.errors) if result.errors else []
    if result.warnings and not errors:
        errors = list(result.warnings)
    return result.passed, errors


def list_installed_packages() -> tuple[bool, list[str]]:
    """Legacy wrapper: List all installed packages.

    Returns:
        Tuple of (passed, errors) for backward compatibility
    """
    checker = InstalledPackagesChecker(verbose=False)
    result = checker.run()
    return result.passed, list(result.errors)


def check_pyproject_dependencies() -> tuple[bool, list[str]]:
    """Legacy wrapper: Check pyproject.toml dependencies.

    Returns:
        Tuple of (passed, errors) for backward compatibility
    """
    checker = PyprojectDependenciesChecker(verbose=False)
    result = checker.run()
    errors = list(result.errors) if result.errors else []
    if result.missing_packages and not errors:
        errors = [f"Missing packages: {', '.join(result.missing_packages)}"]
    return result.passed, errors


if __name__ == "__main__":
    sys.exit(main())
