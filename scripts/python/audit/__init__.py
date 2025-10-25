"""
Python Audit Package

Provides automated code quality auditing and dependency management tools.
Includes checks for code formatting (Black), linting (Ruff), type checking (mypy),
and package dependency validation.

Modules:
    code_quality: Runs Black, Ruff, and mypy checks across the codebase
    dependencies: Checks for outdated packages and validates dependencies

Examples:
    >>> from python.audit import run_black_check, check_outdated_packages
    >>> from python.audit import *  # Exports via __all__

See Also:
    - scripts/orchestrator.py audit code
    - scripts/orchestrator.py audit deps
"""

# Import submodules to make them available in the package namespace
from . import code_quality, dependencies
from .code_quality import (
    main as code_quality_main,
    run_black_check,
    run_mypy_check,
    run_ruff_check,
)
from .dependencies import (
    check_outdated_packages,
    check_pyproject_dependencies,
    list_installed_packages,
    main as dependencies_main,
)

__all__: list[str] = [
    # Submodules
    "code_quality",
    "dependencies",
    # Code quality functions
    "run_black_check",
    "run_ruff_check",
    "run_mypy_check",
    "code_quality_main",
    # Dependency functions
    "check_outdated_packages",
    "check_pyproject_dependencies",
    "list_installed_packages",
    "dependencies_main",
]
