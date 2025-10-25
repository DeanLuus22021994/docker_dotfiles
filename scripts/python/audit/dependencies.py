#!/usr/bin/env python3
"""
Dependencies Audit Script
Checks for outdated packages and displays current versions
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


def check_outdated_packages() -> Tuple[bool, List[str]]:
    """Check for outdated Python packages."""
    print(f"\n{header('=== Checking Outdated Packages ===')}")
    errors: List[str] = []

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--outdated"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.stdout.strip():
            print(warning("Outdated packages found:"))
            print(result.stdout)
            print(info("Run 'pip install --upgrade <package>' to update"))
            errors.append("Outdated packages detected")
            return False, errors

        print(success("All packages are up to date"))
        return True, []

    except FileNotFoundError:
        errors.append("pip not found")
        print(error("pip not found"))
        return False, errors


def list_installed_packages() -> Tuple[bool, List[str]]:
    """List all installed packages and versions."""
    print(f"\n{header('=== Installed Packages ===')}")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True,
            check=False,
        )

        print(result.stdout)
        print(success("Package list retrieved successfully"))
        return True, []

    except FileNotFoundError:
        print(error("pip not found"))
        return False, ["pip not found"]


def check_pyproject_dependencies() -> Tuple[bool, List[str]]:
    """Check if all pyproject.toml dependencies are installed."""
    print(f"\n{header('=== Checking pyproject.toml Dependencies ===')}")
    errors: List[str] = []

    pyproject = Path("pyproject.toml")

    if not pyproject.exists():
        print(info("No pyproject.toml found"))
        return True, []

    required_packages = [
        "black",
        "ruff",
        "mypy",
        "yamllint",
        "pytest",
    ]

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True,
            check=False,
        )

        installed = result.stdout.lower()

        missing: List[str] = []
        for pkg in required_packages:
            if pkg.lower() not in installed:
                missing.append(pkg)

        if missing:
            print(warning(f"Missing required packages: {', '.join(missing)}"))
            print(info(f"Run 'pip install {' '.join(missing)}' to install"))
            errors.append(f"Missing packages: {', '.join(missing)}")
            return False, errors

        print(success("All required dependencies installed"))
        return True, []

    except FileNotFoundError:
        errors.append("pip not found")
        print(error("pip not found"))
        return False, errors


def main() -> int:
    """Run all dependency checks."""
    print(separator())
    print(header("Dependencies Audit"))
    print(separator())

    all_errors: List[str] = []
    all_passed = True

    # Run all checks
    checks = [
        ("Required Dependencies", check_pyproject_dependencies),
        ("Outdated Packages", check_outdated_packages),
        ("Installed Packages", list_installed_packages),
    ]

    for _check_name, check_func in checks:
        passed, errors = check_func()
        if not passed:
            all_passed = False
            all_errors.extend(errors)

    # Final summary
    print(f"\n{separator()}")
    if all_passed:
        print(success("ALL DEPENDENCY CHECKS PASSED"))
        print(separator())
        return 0
    else:
        print(warning(f"DEPENDENCY AUDIT COMPLETED WITH WARNINGS ({len(all_errors)} issue(s))"))
        print(separator())
        print("\nIssues:")
        for err in all_errors:
            print(f"  - {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
