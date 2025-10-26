#!/usr/bin/env python3
"""
Code Quality Audit Script

Runs code quality checks (Black, Ruff, mypy) across the codebase using
a modular checker architecture. Each tool is wrapped in a dedicated checker
class following the Single Responsibility Principle.

This module uses Python 3.14 type system features including dataclasses,
TypeAlias, Protocol, and Final for improved type safety.

Exit code: 0=success, 1=failure

Examples:
    >>> from audit.code_quality import CodeQualityAuditor
    >>> auditor = CodeQualityAuditor()
    >>> report = auditor.run_all_checks()
    >>> print(report.passed)  # True if all checks passed
"""

import subprocess
import sys
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, Protocol, TypeAlias

# Add parent directory to path for imports
_script_dir = Path(__file__).parent.parent.parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

from scripts.python.utils.colors import error, header, info, separator, success, warning

# Type aliases for semantic clarity
ToolName: TypeAlias = str
CommandArgs: TypeAlias = Sequence[str]
ErrorMessage: TypeAlias = str
ExitCode: TypeAlias = int

# Constants
DEFAULT_PYTHON_DIRS: Final[tuple[str, ...]] = ("scripts/python/", "scripts/orchestrator.py")
BLACK_LINE_LENGTH: Final[int] = 100


# Constants
DEFAULT_PYTHON_DIRS: Final[tuple[str, ...]] = ("scripts/python/", "scripts/orchestrator.py")
BLACK_LINE_LENGTH: Final[int] = 100


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Result of a code quality check.

    Attributes:
        passed: Whether the check succeeded
        tool_name: Name of the tool that ran the check
        errors: List of error messages (empty if passed)
        stdout: Raw stdout from tool execution
        install_hint: Installation command if tool not found
    """

    passed: bool
    tool_name: ToolName
    errors: tuple[ErrorMessage, ...] = field(default_factory=tuple)
    stdout: str = ""
    install_hint: str = ""

    @property
    def has_errors(self) -> bool:
        """Check if result contains any errors."""
        return len(self.errors) > 0


@dataclass(frozen=True, slots=True)
class CodeQualityReport:
    """Aggregated results from all code quality checks.

    Attributes:
        results: Tuple of all check results
        total_checks: Total number of checks run
        passed_checks: Number of checks that passed
        failed_checks: Number of checks that failed
    """

    results: tuple[CheckResult, ...]

    @property
    def passed(self) -> bool:
        """Check if all quality checks passed."""
        return all(result.passed for result in self.results)

    @property
    def total_checks(self) -> int:
        """Total number of checks run."""
        return len(self.results)

    @property
    def passed_checks(self) -> int:
        """Number of checks that passed."""
        return sum(1 for result in self.results if result.passed)

    @property
    def failed_checks(self) -> int:
        """Number of checks that failed."""
        return sum(1 for result in self.results if not result.passed)

    @property
    def all_errors(self) -> tuple[ErrorMessage, ...]:
        """Collect all errors from failed checks."""
        errors: list[ErrorMessage] = []
        for result in self.results:
            errors.extend(result.errors)
        return tuple(errors)


class CheckerProtocol(Protocol):
    """Protocol defining interface for code quality checkers."""

    @property
    def tool_name(self) -> ToolName:
        """Name of the quality checking tool."""
        ...

    def run(self, target_paths: Sequence[str]) -> CheckResult:
        """Run the quality check.

        Args:
            target_paths: Paths to check

        Returns:
            CheckResult with pass/fail status and errors
        """
        ...


class BaseChecker(ABC):
    """Abstract base class for code quality checkers.

    Provides common functionality for running subprocess commands
    and handling tool availability.
    """

    def __init__(self, *, verbose: bool = True) -> None:
        """Initialize checker.

        Args:
            verbose: Enable verbose output (default: True)
        """
        self.verbose = verbose

    @property
    @abstractmethod
    def tool_name(self) -> ToolName:
        """Name of the quality checking tool."""
        ...

    @property
    @abstractmethod
    def install_command(self) -> str:
        """Command to install the tool."""
        ...

    @abstractmethod
    def build_command(self, target_paths: Sequence[str]) -> CommandArgs:
        """Build command arguments for the tool.

        Args:
            target_paths: Paths to check

        Returns:
            Command arguments as sequence
        """
        ...

    @abstractmethod
    def format_output(self, result: subprocess.CompletedProcess[str]) -> None:
        """Format and print tool output.

        Args:
            result: Subprocess result from tool execution
        """
        ...

    def run(self, target_paths: Sequence[str]) -> CheckResult:
        """Run the quality check.

        Args:
            target_paths: Paths to check

        Returns:
            CheckResult with pass/fail status and errors
        """
        if self.verbose:
            print(f"\n{header(f'=== Running {self.tool_name} ===')}")

        try:
            cmd = self.build_command(target_paths)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                errors = (f"{self.tool_name} found issues:\n{result.stdout}",)
                if self.verbose:
                    self.format_output(result)
                return CheckResult(
                    passed=False,
                    tool_name=self.tool_name,
                    errors=errors,
                    stdout=result.stdout,
                )

            if self.verbose:
                print(success(f"{self.tool_name} check passed"))
            return CheckResult(passed=True, tool_name=self.tool_name)

        except FileNotFoundError:
            error_msg = f"{self.tool_name} not found"
            if self.verbose:
                print(error(error_msg))
            return CheckResult(
                passed=False,
                tool_name=self.tool_name,
                errors=(error_msg,),
                install_hint=self.install_command,
            )


class BlackChecker(BaseChecker):
    """Black code formatter checker.

    Runs Black in check mode to verify code formatting without
    making changes. Uses 100-character line length.
    """

    @property
    def tool_name(self) -> ToolName:
        return "Black"

    @property
    def install_command(self) -> str:
        return "pip install black"

    def build_command(self, target_paths: Sequence[str]) -> CommandArgs:
        """Build Black command with check flag and line length."""
        return ["black", "--check", f"--line-length={BLACK_LINE_LENGTH}", *target_paths]

    def format_output(self, result: subprocess.CompletedProcess[str]) -> None:
        """Format Black output with fix instructions."""
        print(warning("Black found formatting issues"))
        print(result.stdout)
        print(info("Run 'black scripts/python/ scripts/orchestrator.py' to fix"))


class RuffChecker(BaseChecker):
    """Ruff linter checker.

    Runs Ruff linter to identify code quality issues,
    potential bugs, and style violations.
    """

    @property
    def tool_name(self) -> ToolName:
        return "Ruff"

    @property
    def install_command(self) -> str:
        return "pip install ruff"

    def build_command(self, target_paths: Sequence[str]) -> CommandArgs:
        """Build Ruff command for linting."""
        return ["ruff", "check", *target_paths]

    def format_output(self, result: subprocess.CompletedProcess[str]) -> None:
        """Format Ruff output with fix instructions."""
        print(warning("Ruff found linting issues"))
        print(result.stdout)
        print(info("Run 'ruff check --fix scripts/python/ scripts/orchestrator.py' to fix"))


class MypyChecker(BaseChecker):
    """Mypy type checker.

    Runs mypy in strict mode to verify type annotations
    and catch potential type-related bugs.
    """

    @property
    def tool_name(self) -> ToolName:
        return "mypy"

    @property
    def install_command(self) -> str:
        return "pip install mypy"

    def build_command(self, target_paths: Sequence[str]) -> CommandArgs:
        """Build mypy command with strict mode."""
        return ["mypy", "--strict", *target_paths]

    def format_output(self, result: subprocess.CompletedProcess[str]) -> None:
        """Format mypy output."""
        print(warning("mypy found type errors"))
        print(result.stdout)


class CodeQualityAuditor:
    """Orchestrates code quality checks across multiple tools.

    Runs Black, Ruff, and mypy checks and aggregates results
    into a comprehensive report.

    Example:
        >>> auditor = CodeQualityAuditor()
        >>> report = auditor.run_all_checks()
        >>> if report.passed:
        ...     print("All checks passed!")
    """

    def __init__(
        self,
        *,
        target_paths: Sequence[str] = DEFAULT_PYTHON_DIRS,
        verbose: bool = True,
    ) -> None:
        """Initialize auditor with checkers.

        Args:
            target_paths: Paths to check (default: scripts/python/)
            verbose: Enable verbose output (default: True)
        """
        self.target_paths = target_paths
        self.verbose = verbose
        self.checkers: tuple[BaseChecker, ...] = (
            BlackChecker(verbose=verbose),
            RuffChecker(verbose=verbose),
            MypyChecker(verbose=verbose),
        )

    def run_all_checks(self) -> CodeQualityReport:
        """Run all configured code quality checks.

        Returns:
            CodeQualityReport with aggregated results
        """
        if self.verbose:
            print(separator())
            print(header("Code Quality Audit"))
            print(separator())

        results: list[CheckResult] = []
        for checker in self.checkers:
            result = checker.run(self.target_paths)
            results.append(result)

        return CodeQualityReport(results=tuple(results))

    def print_summary(self, report: CodeQualityReport) -> None:
        """Print human-readable summary of audit results.

        Args:
            report: Report to summarize
        """
        print(f"\n{separator()}")
        if report.passed:
            print(success("ALL CODE QUALITY CHECKS PASSED"))
        else:
            print(error(f"CODE QUALITY AUDIT FAILED ({report.failed_checks}/{report.total_checks} checks)"))

        print(separator())

        if not report.passed and report.all_errors:
            print("\nIssues:")
            for err in report.all_errors:
                print(f"  - {err}")

            # Print install hints for missing tools
            for result in report.results:
                if result.install_hint:
                    print(f"\nInstall {result.tool_name}: {result.install_hint}")


def main() -> ExitCode:
    """Run all code quality checks and return exit code.

    Returns:
        0 if all checks passed, 1 otherwise
    """
    auditor = CodeQualityAuditor()
    report = auditor.run_all_checks()
    auditor.print_summary(report)

    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
