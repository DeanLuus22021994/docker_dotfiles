#!/usr/bin/env python3
"""Test script for document generator functionality.

This script validates that the document templates and schemas work correctly
even when optional dependencies are not available.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

from ..schemas.frontmatter import DocFrontmatter
from .new_doc import CATEGORIES


def test_basic_functionality() -> bool:
    """Test basic functionality without external dependencies."""
    print("Testing document generator basic functionality...")

    try:
        # Test schema import
        print("✅ Schema imports successful")

        # Test frontmatter creation
        now = datetime.now(timezone.utc)
        frontmatter = DocFrontmatter(
            title="Test Document",
            date_created=now,
            last_updated=now,
            tags=["testing", "documentation"],
            description="Test document for validation",
        )
        print(f"✅ Frontmatter creation successful: {frontmatter.tags}")

        # Test template directory exists
        template_dir = Path(__file__).parent.parent / "templates"
        if template_dir.exists():
            templates = list(template_dir.glob("*.j2"))
            print(f"✅ Templates directory exists with {len(templates)} templates")
        else:
            print("❌ Templates directory not found")
            return False

        # Test categories structure
        print(f"✅ Document categories loaded: {len(CATEGORIES)} categories")

        return True

    except (ImportError, ValueError, AttributeError) as e:
        print(f"❌ Error: {e}")
        return False


def test_template_rendering() -> bool:
    """Test template rendering with fallbacks."""
    print("\\nTesting template rendering...")

    try:
        # Test basic template loading
        template_dir = Path(__file__).parent.parent / "templates"
        base_template = template_dir / "base.j2"

        if base_template.exists():
            content = base_template.read_text(encoding="utf-8")
            if "{{ title }}" in content and "{{ description }}" in content:
                print("✅ Template structure is valid")
                return True
            else:
                print("❌ Template missing required variables")
                return False
        else:
            print("❌ Base template not found")
            return False

    except (OSError, UnicodeDecodeError) as e:
        print(f"❌ Template test failed: {e}")
        return False


def test_snippets_integration() -> bool:
    """Test VS Code snippets integration."""
    print("\\nTesting VS Code snippets...")

    try:
        snippets_file = (
            Path(__file__).parent.parent.parent.parent
            / ".vscode"
            / "snippets"
            / "mkdocs.code-snippets"
        )

        if snippets_file.exists():
            content = snippets_file.read_text(encoding="utf-8")
            if "MkDocs Frontmatter" in content and "mkdocs-front" in content:
                print("✅ VS Code snippets are properly configured")
                return True
            else:
                print("❌ Snippets missing required entries")
                return False
        else:
            print("❌ Snippets file not found")
            return False

    except (OSError, UnicodeDecodeError) as e:
        print(f"❌ Snippets test failed: {e}")
        return False


if __name__ == "__main__":
    print("MkDocs Document Generator Test Suite")
    print("=" * 40)

    tests = [test_basic_functionality, test_template_rendering, test_snippets_integration]

    PASSED = 0
    TOTAL = len(tests)

    for test in tests:
        if test():
            PASSED += 1

    print(f"\\nResults: {PASSED}/{TOTAL} tests passed")

    if PASSED == TOTAL:
        print("🎉 All tests passed! Document generator is ready.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check configuration.")
        sys.exit(1)
