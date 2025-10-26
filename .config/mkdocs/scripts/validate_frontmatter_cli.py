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

import yaml


def validate_frontmatter(file_path: Path) -> tuple[bool, list[str]]:
    """
    Validate frontmatter in a markdown file.

    Args:
        file_path: Path to markdown file

    Returns:
        Tuple of (is_valid, errors)
    """
    required_fields = frozenset({"title", "description"})
    errors: list[str] = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError as e:
        return False, [f"Error reading file: {e}"]

    # Check for frontmatter
    if not content.startswith("---"):
        return False, ["Missing frontmatter delimiter '---'"]

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False, ["Incomplete frontmatter (missing closing '---')"]

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return False, [f"Invalid YAML in frontmatter: {e}"]

    if not isinstance(frontmatter, dict):
        return False, ["Frontmatter must be a YAML mapping"]

    # Check required fields
    missing_fields = required_fields - frontmatter.keys()
    if missing_fields:
        errors.append(f"Missing required fields: {', '.join(sorted(missing_fields))}")

    # Validate field types
    if "title" in frontmatter and not isinstance(frontmatter["title"], str):
        errors.append("Field 'title' must be a string")

    if "description" in frontmatter and not isinstance(frontmatter["description"], str):
        errors.append("Field 'description' must be a string")

    if "tags" in frontmatter and not isinstance(frontmatter["tags"], list):
        errors.append("Field 'tags' must be a list")

    return len(errors) == 0, errors


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

        is_valid, errors = validate_frontmatter(file_path)

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
