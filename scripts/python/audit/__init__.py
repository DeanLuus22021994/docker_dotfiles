"""
Python Audit Package

Provides automated code quality auditing and dependency management tools.
Includes checks for code formatting (Black), linting (Ruff), type checking (mypy),
and package dependency validation.

Modules:
    code_quality: Runs Black, Ruff, and mypy checks across the codebase
    dependencies: Checks for outdated packages and validates dependencies

Examples:
    >>> from python.audit import code_quality, dependencies
    >>> from python.audit import *  # Exports via __all__

See Also:
    - scripts/orchestrator.py audit code
    - scripts/orchestrator.py audit deps
"""

# Import submodules to make them available in the package namespace
from . import code_quality, dependencies

__all__: list[str] = ["code_quality", "dependencies"]
