#!/usr/bin/env python3
"""
Code Quality Audit Script
Runs Black, Ruff, and mypy checks across the codebase
Exit code: 0=success, 1=failure
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Add parent directory to path for imports
_script_dir = Path(__file__).parent.parent.parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

from python.utils.colors import error, header, info, separator, success, warning


def run_black_check() -> Tuple[bool, List[str]]:
    """Run Black formatter in check mode."""
    print(f"\n{header('=== Running Black Format Check ===')}")
    errors: List[str] = []

    python_dirs = ["scripts/python/", "scripts/orchestrator.py"]

    try:
        result = subprocess.run(
            ["black", "--check", "--line-length=100"] + python_dirs,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            errors.append(f"Black formatting issues found:\n{result.stdout}")
            print(warning("Black found formatting issues"))
            print(result.stdout)
            print(info("Run 'black scripts/python/ scripts/orchestrator.py' to fix"))
            return False, errors

        print(success("Black formatting check passed"))
        return True, []

    except FileNotFoundError:
        errors.append("Black not found. Install with: pip install black")
        print(error("Black not found"))
        return False, errors


def run_ruff_check() -> Tuple[bool, List[str]]:
    """Run Ruff linter."""
    print(f"\n{header('=== Running Ruff Linter ===')}")
    errors: List[str] = []

    python_dirs = ["scripts/python/", "scripts/orchestrator.py"]

    try:
        result = subprocess.run(
            ["ruff", "check"] + python_dirs,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            errors.append(f"Ruff found linting issues:\n{result.stdout}")
            print(warning("Ruff found linting issues"))
            print(result.stdout)
            print(info("Run 'ruff check --fix scripts/python/ scripts/orchestrator.py' to fix"))
            return False, errors

        print(success("Ruff linting check passed"))
        return True, []

    except FileNotFoundError:
        errors.append("Ruff not found. Install with: pip install ruff")
        print(error("Ruff not found"))
        return False, errors


def run_mypy_check() -> Tuple[bool, List[str]]:
    """Run mypy type checker."""
    print(f"\n{header('=== Running mypy Type Check ===')}")
    errors: List[str] = []

    python_dirs = ["scripts/python/", "scripts/orchestrator.py"]

    try:
        result = subprocess.run(
            ["mypy", "--strict"] + python_dirs,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            errors.append(f"mypy found type errors:\n{result.stdout}")
            print(warning("mypy found type errors"))
            print(result.stdout)
            return False, errors

        print(success("mypy type check passed"))
        return True, []

    except FileNotFoundError:
        errors.append("mypy not found. Install with: pip install mypy")
        print(error("mypy not found"))
        return False, errors


def main() -> int:
    """Run all code quality checks."""
    print(separator())
    print(header("Code Quality Audit"))
    print(separator())

    all_errors: List[str] = []
    all_passed = True

    # Run all checks
    checks = [
        ("Black", run_black_check),
        ("Ruff", run_ruff_check),
        ("mypy", run_mypy_check),
    ]

    for _check_name, check_func in checks:
        passed, errors = check_func()
        if not passed:
            all_passed = False
            all_errors.extend(errors)

    # Final summary
    print(f"\n{separator()}")
    if all_passed:
        print(success("ALL CODE QUALITY CHECKS PASSED"))
        print(separator())
        return 0
    else:
        print(error(f"CODE QUALITY AUDIT FAILED ({len(all_errors)} issue(s))"))
        print(separator())
        print("\nIssues:")
        for err in all_errors:
            print(f"  - {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
