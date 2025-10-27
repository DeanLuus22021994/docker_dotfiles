#!/usr/bin/env python3
"""
Frontmatter Validation CLI
==========================

Command-line interface for validating markdown frontmatter.
Used by pre-commit hooks to enforce frontmatter requirements.

Usage:
    python validate_frontmatter_cli.py file1.md file2.md ...

Exit codes:
    0: All files valid
    1: Validation errors found
"""

import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..hooks.validate_frontmatter import validate_file_frontmatter
else:
    try:
        from ..hooks.validate_frontmatter import (
            validate_file_frontmatter,
        )
    except ImportError:  # pragma: no cover - fallback for direct execution
        current_dir = Path(__file__).resolve().parents[1]
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))
        from hooks.validate_frontmatter import validate_file_frontmatter


def main() -> int:
    """Main entry point for CLI."""
    if len(sys.argv) < 2:
        print("Usage: validate_frontmatter_cli.py file1.md file2.md ...", file=sys.stderr)
        return 1

    all_valid = True
    for file_arg in sys.argv[1:]:
        file_path = Path(file_arg)

        if not file_path.exists():
            print(f"❌ {file_path}: File not found", file=sys.stderr)
            all_valid = False
            continue

        is_valid, errors = validate_file_frontmatter(file_path)

        if not is_valid:
            print(f"❌ {file_path}:", file=sys.stderr)
            for error in errors:
                print(f"   • {error}", file=sys.stderr)
            all_valid = False
        else:
            print(f"✅ {file_path}: Valid frontmatter")

    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
