"""
Python Audit Package

Provides automated code quality auditing and dependency management tools
using modular checker classes. Each audit type is handled by dedicated
classes following the Single Responsibility Principle.

Modules:
    code_quality: Runs Black, Ruff, and mypy checks with CodeQualityAuditor
    dependencies: Checks packages with DependencyAuditor

Examples:
    >>> from python.audit import CodeQualityAuditor, DependencyAuditor
    >>> auditor = CodeQualityAuditor()
    >>> report = auditor.run_all_checks()
    >>> print(report.passed)

See Also:
    - scripts/orchestrator.py audit code
    - scripts/orchestrator.py audit deps
"""

# Import submodules to make them available in the package namespace
from . import code_quality, dependencies

# Import new class-based APIs
from .code_quality import (
    BLACK_LINE_LENGTH,
    BaseChecker,
    BlackChecker,
    CheckResult,
    CodeQualityAuditor,
    CodeQualityReport,
    DEFAULT_PYTHON_DIRS,
    MypyChecker,
    RuffChecker,
    main as code_quality_main,
    # Legacy function wrappers for backward compatibility
    run_black_check,
    run_mypy_check,
    run_ruff_check,
)
from .dependencies import (
    BaseDependencyChecker,
    DependencyAuditor,
    DependencyCheckResult,
    DependencyReport,
    InstalledPackagesChecker,
    OutdatedPackagesChecker,
    Package,
    PyprojectDependenciesChecker,
    PYPROJECT_PATH,
    REQUIRED_PACKAGES,
    main as dependencies_main,
    # Legacy function wrappers for backward compatibility
    check_outdated_packages,
    check_pyproject_dependencies,
    list_installed_packages,
)

__all__: list[str] = [
    # Submodules
    "code_quality",
    "dependencies",
    # Code quality classes and constants
    "CodeQualityAuditor",
    "BaseChecker",
    "BlackChecker",
    "RuffChecker",
    "MypyChecker",
    "CheckResult",
    "CodeQualityReport",
    "DEFAULT_PYTHON_DIRS",
    "BLACK_LINE_LENGTH",
    "code_quality_main",
    # Legacy code quality functions (backward compatibility)
    "run_black_check",
    "run_ruff_check",
    "run_mypy_check",
    # Dependency classes and constants
    "DependencyAuditor",
    "BaseDependencyChecker",
    "OutdatedPackagesChecker",
    "InstalledPackagesChecker",
    "PyprojectDependenciesChecker",
    "Package",
    "DependencyCheckResult",
    "DependencyReport",
    "REQUIRED_PACKAGES",
    "PYPROJECT_PATH",
    "dependencies_main",
    # Legacy dependency functions (backward compatibility)
    "check_outdated_packages",
    "list_installed_packages",
    "check_pyproject_dependencies",
]
