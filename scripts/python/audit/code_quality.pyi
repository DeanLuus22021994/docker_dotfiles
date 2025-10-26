"""Type stubs for code_quality module.

Provides type hints for code quality checking utilities.
"""

import subprocess
from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final, Protocol, TypeAlias

# Type aliases
ToolName: TypeAlias = str
CommandArgs: TypeAlias = Sequence[str]
ErrorMessage: TypeAlias = str
ExitCode: TypeAlias = int

# Constants
DEFAULT_PYTHON_DIRS: Final[tuple[str, ...]]
BLACK_LINE_LENGTH: Final[int]

@dataclass(frozen=True, slots=True)
class CheckResult:
    """Result of a code quality check."""

    passed: bool
    tool_name: ToolName
    errors: tuple[ErrorMessage, ...]
    stdout: str
    install_hint: str

    @property
    def has_errors(self) -> bool:
        """Check if any errors exist."""

@dataclass(frozen=True, slots=True)
class CodeQualityReport:
    """Aggregated results from all code quality checks."""

    results: tuple[CheckResult, ...]

    @property
    def passed(self) -> bool:
        """Check if all checks passed."""
    @property
    def total_checks(self) -> int:
        """Total number of checks run."""
    @property
    def passed_checks(self) -> int:
        """Number of passed checks."""
    @property
    def failed_checks(self) -> int:
        """Number of failed checks."""
    @property
    def all_errors(self) -> tuple[ErrorMessage, ...]:
        """All error messages combined."""

class CheckerProtocol(Protocol):
    """Protocol for code quality checkers."""

    @property
    def tool_name(self) -> ToolName:
        """Name of the checking tool."""
    def run(self, _target_paths: Sequence[str], /) -> CheckResult:
        """Run the checker."""

class BaseChecker(ABC):
    """Abstract base class for code quality checkers."""

    verbose: bool

    @property
    def tool_name(self) -> ToolName:
        """Name of the checking tool."""
    @property
    def install_command(self) -> str:
        """Command to install the tool."""
    def build_command(self, target_paths: Sequence[str], /) -> CommandArgs:
        """Build command arguments."""
    def format_output(self, result: subprocess.CompletedProcess[str], /) -> None:
        """Format tool output."""
    def run(self, target_paths: Sequence[str], /) -> CheckResult:
        """Run the checker."""

class BlackChecker(BaseChecker):
    """Black code formatter checker."""

    @property
    def tool_name(self) -> ToolName:
        """Name of the checking tool."""
    @property
    def install_command(self) -> str:
        """Command to install Black."""
    def build_command(self, target_paths: Sequence[str], /) -> CommandArgs:
        """Build Black command arguments."""
    def format_output(self, result: subprocess.CompletedProcess[str], /) -> None:
        """Format Black output."""

class RuffChecker(BaseChecker):
    """Ruff linter checker."""

    @property
    def tool_name(self) -> ToolName:
        """Name of the checking tool."""
    @property
    def install_command(self) -> str:
        """Command to install Ruff."""
    def build_command(self, target_paths: Sequence[str], /) -> CommandArgs:
        """Build Ruff command arguments."""
    def format_output(self, result: subprocess.CompletedProcess[str], /) -> None:
        """Format Ruff output."""

class MypyChecker(BaseChecker):
    """Mypy type checker."""

    @property
    def tool_name(self) -> ToolName:
        """Name of the checking tool."""
    @property
    def install_command(self) -> str:
        """Command to install mypy."""
    def build_command(self, target_paths: Sequence[str], /) -> CommandArgs:
        """Build mypy command arguments."""
    def format_output(self, result: subprocess.CompletedProcess[str], /) -> None:
        """Format mypy output."""

class CodeQualityAuditor:
    """Orchestrates code quality checks."""

    target_paths: Sequence[str]
    verbose: bool
    checkers: tuple[BaseChecker, ...]

    def run_all_checks(self) -> CodeQualityReport:
        """Run all configured code quality checks."""
    def print_summary(self, report: CodeQualityReport, /) -> None:
        """Print summary of check results."""

def run_black_check() -> tuple[bool, list[str]]:
    """Run Black format check."""

def run_ruff_check() -> tuple[bool, list[str]]:
    """Run Ruff lint check."""

def run_mypy_check() -> tuple[bool, list[str]]:
    """Run mypy type check."""

def main() -> ExitCode:
    """Run all code quality checks."""

__all__: list[str]
