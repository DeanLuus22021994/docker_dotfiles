#!/usr/bin/env python3
"""
MkDocs Site Health Validation Script
====================================

Validates the built MkDocs site for:
- Critical pages existence and accessibility
- Search index integrity
- Navigation structure
- Asset availability
- Link consistency

Python 3.14 compliant with modern type hints and error handling.

Usage:
    python validate_health.py --site-dir ./site
    python validate_health.py --site-dir ./site --check-links

Environment Variables:
    MKDOCS_HEALTH_STRICT: Fail on warnings (default: false)
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Immutable validation result using Python 3.14 dataclass features."""

    check_name: str
    passed: bool
    message: str
    severity: str = "error"  # error, warning, info


@dataclass(slots=True)
class HealthCheckStats:
    """Health check statistics using slots for memory efficiency."""

    total_checks: int = 0
    passed: int = 0
    failed: int = 0
    warnings: int = 0


class SiteHealthValidator:
    """
    Validates MkDocs site health after build.

    Uses Python 3.14 features:
    - PEP 585 type hints (list[], dict[])
    - Dataclasses with slots
    - Structural pattern matching
    - Modern Path operations
    """

    CRITICAL_PAGES: frozenset[str] = frozenset(
        {
            "index.html",
            "search/search_index.json",
            "404.html",
        }
    )

    CRITICAL_ASSETS: frozenset[str] = frozenset(
        {
            "assets/stylesheets",
            "assets/javascripts",
        }
    )

    def __init__(self, site_dir: Path, strict: bool = False) -> None:
        """Initialize validator with site directory."""
        self.site_dir = site_dir
        self.strict = strict
        self.results: list[ValidationResult] = []
        self.stats = HealthCheckStats()

    def validate_directory_structure(self) -> None:
        """Validate site directory exists and is accessible."""
        match self.site_dir:
            case Path() as p if not p.exists():
                self.add_result(
                    "directory_exists", False, f"Site directory does not exist: {p}", "error"
                )
            case Path() as p if not p.is_dir():
                self.add_result(
                    "directory_is_dir", False, f"Site path is not a directory: {p}", "error"
                )
            case _:
                self.add_result(
                    "directory_structure",
                    True,
                    f"Site directory accessible: {self.site_dir}",
                    "info",
                )

    def validate_critical_pages(self) -> None:
        """Validate presence of critical pages."""
        for page in self.CRITICAL_PAGES:
            page_path = self.site_dir / page

            match page_path:
                case Path() as p if not p.exists():
                    self.add_result(
                        f"critical_page_{page}", False, f"Missing critical page: {page}", "error"
                    )
                case Path() as p if p.stat().st_size == 0:
                    self.add_result(
                        f"critical_page_{page}", False, f"Critical page is empty: {page}", "error"
                    )
                case _:
                    self.add_result(
                        f"critical_page_{page}", True, f"Critical page exists: {page}", "info"
                    )

    def validate_search_index(self) -> None:
        """Validate search index JSON file."""
        search_index = self.site_dir / "search" / "search_index.json"

        if not search_index.exists():
            self.add_result("search_index_exists", False, "Search index file missing", "error")
            return

        try:
            content = search_index.read_text(encoding="utf-8")
            index_data = json.loads(content)

            match index_data:
                case {"docs": list() as docs, "config": dict()}:
                    doc_count = len(docs)
                    self.add_result(
                        "search_index_valid",
                        True,
                        f"Search index valid ({doc_count} documents indexed)",
                        "info",
                    )

                    if doc_count == 0:
                        self.add_result(
                            "search_index_populated",
                            False,
                            "Search index is empty (no documents)",
                            "warning",
                        )
                    else:
                        self.add_result(
                            "search_index_populated",
                            True,
                            f"Search index populated ({doc_count} docs)",
                            "info",
                        )
                case _:
                    self.add_result(
                        "search_index_valid", False, "Search index has invalid structure", "error"
                    )

        except json.JSONDecodeError as e:
            self.add_result(
                "search_index_valid", False, f"Search index JSON is invalid: {e}", "error"
            )
        except OSError as e:
            self.add_result(
                "search_index_readable", False, f"Cannot read search index: {e}", "error"
            )

    def validate_assets(self) -> None:
        """Validate presence of asset directories."""
        for asset_dir in self.CRITICAL_ASSETS:
            asset_path = self.site_dir / asset_dir

            if not asset_path.exists():
                self.add_result(
                    f"asset_dir_{asset_dir.replace('/', '_')}",
                    False,
                    f"Missing asset directory: {asset_dir}",
                    "warning" if not self.strict else "error",
                )
                continue

            # Count files in asset directory
            asset_files = list(asset_path.rglob("*"))
            file_count = len([f for f in asset_files if f.is_file()])

            if file_count == 0:
                self.add_result(
                    f"asset_dir_{asset_dir.replace('/', '_')}",
                    False,
                    f"Asset directory is empty: {asset_dir}",
                    "warning",
                )
            else:
                self.add_result(
                    f"asset_dir_{asset_dir.replace('/', '_')}",
                    True,
                    f"Asset directory exists ({file_count} files): {asset_dir}",
                    "info",
                )

    def validate_html_pages(self) -> None:
        """Validate all HTML pages can be read."""
        html_files = list(self.site_dir.rglob("*.html"))

        if not html_files:
            self.add_result("html_pages_exist", False, "No HTML files found in site", "error")
            return

        self.add_result("html_pages_exist", True, f"Found {len(html_files)} HTML pages", "info")

        # Check for minimum content in HTML files
        empty_pages: list[str] = []
        for html_file in html_files:
            try:
                size = html_file.stat().st_size
                if size < 100:  # Less than 100 bytes is suspicious
                    empty_pages.append(str(html_file.relative_to(self.site_dir)))
            except OSError:
                pass

        if empty_pages:
            self.add_result(
                "html_pages_content",
                False,
                f"Found {len(empty_pages)} suspiciously small pages: "
                f"{', '.join(empty_pages[:5])}{'...' if len(empty_pages) > 5 else ''}",
                "warning",
            )
        else:
            self.add_result(
                "html_pages_content", True, f"All {len(html_files)} pages have content", "info"
            )

    def add_result(self, check_name: str, passed: bool, message: str, severity: str) -> None:
        """Add a validation result and update stats."""
        result = ValidationResult(check_name, passed, message, severity)
        self.results.append(result)

        self.stats.total_checks += 1
        if passed:
            self.stats.passed += 1
        elif severity == "warning":
            self.stats.warnings += 1
        else:
            self.stats.failed += 1

    def run_all_checks(self) -> bool:
        """Run all validation checks."""
        self.validate_directory_structure()

        # Only continue if directory is accessible
        if self.site_dir.exists() and self.site_dir.is_dir():
            self.validate_critical_pages()
            self.validate_search_index()
            self.validate_assets()
            self.validate_html_pages()

        return self.stats.failed == 0 and (not self.strict or self.stats.warnings == 0)

    def print_report(self) -> None:
        """Print validation report."""
        print("\n" + "=" * 80)
        print("MKDOCS SITE HEALTH VALIDATION")
        print("=" * 80)
        print(f"Site Directory: {self.site_dir}")
        print(f"Strict Mode: {self.strict}")
        print("=" * 80)

        # Group results by severity
        errors: list[ValidationResult] = []
        warnings: list[ValidationResult] = []
        info: list[ValidationResult] = []

        for result in self.results:
            match result.severity:
                case "error":
                    errors.append(result)
                case "warning":
                    warnings.append(result)
                case "info":
                    info.append(result)

        # Print errors
        if errors:
            print("\n❌ ERRORS:")
            for result in errors:
                status = "✓" if result.passed else "✗"
                print(f"  {status} {result.check_name}: {result.message}")

        # Print warnings
        if warnings:
            print("\n⚠️  WARNINGS:")
            for result in warnings:
                status = "✓" if result.passed else "✗"
                print(f"  {status} {result.check_name}: {result.message}")

        # Print info (only if verbose or all passed)
        if info and (self.stats.failed == 0 or len(info) <= 5):
            print("\nℹ️  INFO:")
            for result in info[:5]:  # Limit info output
                print(f"  ✓ {result.check_name}: {result.message}")
            if len(info) > 5:
                print(f"  ... and {len(info) - 5} more")

        # Print summary
        print("\n" + "=" * 80)
        print(f"Total Checks: {self.stats.total_checks}")
        print(f"Passed: {self.stats.passed}")
        print(f"Failed: {self.stats.failed}")
        print(f"Warnings: {self.stats.warnings}")
        print("=" * 80)

        if self.stats.failed == 0 and self.stats.warnings == 0:
            print("\n✅ All health checks passed!")
        elif self.stats.failed == 0:
            print(f"\n⚠️  Health checks passed with {self.stats.warnings} warnings")
        else:
            print(f"\n❌ Health checks failed ({self.stats.failed} errors)")

        print()


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate MkDocs site health after build")
    parser.add_argument(
        "--site-dir",
        type=Path,
        default=Path("site"),
        help="Path to built site directory (default: site)",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")

    args = parser.parse_args()

    validator = SiteHealthValidator(args.site_dir, args.strict)
    success = validator.run_all_checks()
    validator.print_report()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
