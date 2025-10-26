"""
Post-Build Health Validation for MkDocs
=======================================

Validates that the generated site meets quality and performance standards.
Performs comprehensive checks on HTML, links, accessibility, and SEO.

Usage:
    python .config/mkdocs/build/validate_health.py
    python .config/mkdocs/build/validate_health.py --site-dir site --strict
"""

import re
import sys
import time
import argparse
import json
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict

import requests

try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


@dataclass
class ValidationResult:
    """Single validation result."""

    category: str
    severity: str  # 'error', 'warning', 'info'
    message: str
    file_path: str | None = None
    line_number: int | None = None


@dataclass
class HealthReport:
    """Comprehensive health report."""

    timestamp: str
    total_files_checked: int
    total_errors: int
    total_warnings: int
    validation_time_seconds: float

    # Category results
    html_validation_results: List[ValidationResult]
    link_validation_results: List[ValidationResult]
    accessibility_results: List[ValidationResult]
    seo_results: List[ValidationResult]
    performance_results: List[ValidationResult]

    # Summary scores
    html_score: float
    link_score: float
    accessibility_score: float
    seo_score: float
    performance_score: float
    overall_score: float

    # Status
    is_healthy: bool


class HTMLValidator:
    """Validates HTML structure and content."""

    def __init__(self) -> None:
        self.results: List[ValidationResult] = []

    def validate_file(self, file_path: Path) -> List[ValidationResult]:
        """Validate a single HTML file."""
        results = []

        try:
            content = file_path.read_text(encoding="utf-8")

            # Basic HTML structure checks
            if not content.strip().startswith("<!DOCTYPE"):
                results.append(
                    ValidationResult(
                        category="html",
                        severity="warning",
                        message="Missing DOCTYPE declaration",
                        file_path=str(file_path),
                    )
                )

            # Check for required meta tags
            if "<meta charset=" not in content:
                results.append(
                    ValidationResult(
                        category="html",
                        severity="error",
                        message="Missing charset meta tag",
                        file_path=str(file_path),
                    )
                )

            if '<meta name="viewport"' not in content:
                results.append(
                    ValidationResult(
                        category="html",
                        severity="warning",
                        message="Missing viewport meta tag",
                        file_path=str(file_path),
                    )
                )

            # Check for title tag
            if "<title>" not in content or content.count("<title>") > 1:
                results.append(
                    ValidationResult(
                        category="html",
                        severity="error",
                        message="Missing or duplicate title tag",
                        file_path=str(file_path),
                    )
                )

            # Check for empty title
            title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
            if title_match and not title_match.group(1).strip():
                results.append(
                    ValidationResult(
                        category="html",
                        severity="error",
                        message="Empty title tag",
                        file_path=str(file_path),
                    )
                )

            # Check for basic accessibility
            if "lang=" not in content:
                results.append(
                    ValidationResult(
                        category="accessibility",
                        severity="warning",
                        message="Missing lang attribute on html element",
                        file_path=str(file_path),
                    )
                )

            # Check for images without alt text
            img_without_alt = re.findall(r"<img(?![^>]*alt=)[^>]*>", content, re.IGNORECASE)
            for _ in img_without_alt:
                results.append(
                    ValidationResult(
                        category="accessibility",
                        severity="warning",
                        message="Image without alt text",
                        file_path=str(file_path),
                    )
                )

        except (OSError, UnicodeDecodeError) as e:
            results.append(
                ValidationResult(
                    category="html",
                    severity="error",
                    message=f"Failed to validate HTML: {e}",
                    file_path=str(file_path),
                )
            )

        return results


class LinkValidator:
    """Validates internal and external links."""

    def __init__(self, site_dir: Path, base_url: str = ""):
        self.site_dir = site_dir
        self.base_url = base_url
        self.session = requests.Session()
        self.checked_urls: Dict[str, bool] = {}

    def validate_links_in_file(self, file_path: Path) -> List[ValidationResult]:
        """Validate links in a single HTML file."""
        results = []

        try:
            content = file_path.read_text(encoding="utf-8")

            # Find all links
            href_links = re.findall(r'href=["\']([^"\']+)["\']', content, re.IGNORECASE)
            src_links = re.findall(r'src=["\']([^"\']+)["\']', content, re.IGNORECASE)

            all_links = set(href_links + src_links)

            for link in all_links:
                # Skip anchors, javascript, mailto, tel
                if link.startswith(("#", "javascript:", "mailto:", "tel:")):
                    continue

                if link.startswith("http"):
                    # External link - check if reachable
                    result = self.check_external_link(link)
                    if result:
                        result.file_path = str(file_path)
                        results.append(result)
                else:
                    # Internal link - check if file exists
                    result = self.check_internal_link(link, file_path)
                    if result:
                        result.file_path = str(file_path)
                        results.append(result)

        except (OSError, UnicodeDecodeError) as e:
            results.append(
                ValidationResult(
                    category="links",
                    severity="error",
                    message=f"Failed to validate links: {e}",
                    file_path=str(file_path),
                )
            )

        return results

    def check_internal_link(self, link: str, current_file: Path) -> ValidationResult | None:
        """Check if internal link exists."""
        # Remove anchor part
        link_path = link.split("#")[0]
        if not link_path:
            return None

        # Resolve relative to current file
        if link_path.startswith("/"):
            target_path = self.site_dir / link_path.lstrip("/")
        else:
            target_path = current_file.parent / link_path

        # Normalize path
        try:
            target_path = target_path.resolve()
        except OSError:
            return ValidationResult(
                category="links", severity="error", message=f"Invalid link path: {link}"
            )

        # Check if target exists
        if not target_path.exists():
            return ValidationResult(
                category="links", severity="error", message=f"Broken internal link: {link}"
            )

        return None

    def check_external_link(self, url: str) -> ValidationResult | None:
        """Check if external link is reachable."""
        # Use cache to avoid repeated checks
        if url in self.checked_urls:
            return (
                None
                if self.checked_urls[url]
                else ValidationResult(
                    category="links",
                    severity="warning",
                    message=f"External link not reachable: {url}",
                )
            )

        try:
            response = self.session.head(url, allow_redirects=True)
            is_reachable = response.status_code < 400
            self.checked_urls[url] = is_reachable

            if not is_reachable:
                return ValidationResult(
                    category="links",
                    severity="warning",
                    message=f"External link returned {response.status_code}: {url}",
                )

        except requests.RequestException:
            self.checked_urls[url] = False
            return ValidationResult(
                category="links", severity="warning", message=f"External link not reachable: {url}"
            )

        return None


class SEOValidator:
    """Validates SEO-related elements."""

    def validate_file(self, file_path: Path) -> List[ValidationResult]:
        """Validate SEO elements in HTML file."""
        results = []

        try:
            content = file_path.read_text(encoding="utf-8")

            # Check meta description
            if '<meta name="description"' not in content.lower():
                results.append(
                    ValidationResult(
                        category="seo",
                        severity="warning",
                        message="Missing meta description",
                        file_path=str(file_path),
                    )
                )
            else:
                desc_match = re.search(
                    r'<meta name="description" content="([^"]*)"', content, re.IGNORECASE
                )
                if desc_match:
                    desc_content = desc_match.group(1)
                    if len(desc_content) < 120:
                        results.append(
                            ValidationResult(
                                category="seo",
                                severity="info",
                                message="Meta description is short (< 120 chars)",
                                file_path=str(file_path),
                            )
                        )
                    elif len(desc_content) > 160:
                        results.append(
                            ValidationResult(
                                category="seo",
                                severity="warning",
                                message="Meta description is too long (> 160 chars)",
                                file_path=str(file_path),
                            )
                        )

            # Check for heading structure
            h1_count = content.lower().count("<h1")
            if h1_count == 0:
                results.append(
                    ValidationResult(
                        category="seo",
                        severity="warning",
                        message="No H1 heading found",
                        file_path=str(file_path),
                    )
                )
            elif h1_count > 1:
                results.append(
                    ValidationResult(
                        category="seo",
                        severity="warning",
                        message="Multiple H1 headings found",
                        file_path=str(file_path),
                    )
                )

            # Check for canonical URL
            if '<link rel="canonical"' not in content.lower():
                results.append(
                    ValidationResult(
                        category="seo",
                        severity="info",
                        message="Missing canonical URL",
                        file_path=str(file_path),
                    )
                )

        except (OSError, UnicodeDecodeError) as e:
            results.append(
                ValidationResult(
                    category="seo",
                    severity="error",
                    message=f"Failed to validate SEO: {e}",
                    file_path=str(file_path),
                )
            )

        return results


class PerformanceValidator:
    """Validates performance-related aspects."""

    def validate_file(self, file_path: Path) -> List[ValidationResult]:
        """Validate performance aspects of HTML file."""
        results = []

        try:
            content = file_path.read_text(encoding="utf-8")

            # Check file size
            file_size = len(content.encode("utf-8"))
            if file_size > 1024 * 1024:  # 1MB
                results.append(
                    ValidationResult(
                        category="performance",
                        severity="warning",
                        message=f"Large HTML file: {file_size / 1024 / 1024:.1f}MB",
                        file_path=str(file_path),
                    )
                )

            # Check for inline CSS/JS
            inline_css_size = sum(
                len(match) for match in re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
            )
            if inline_css_size > 10240:  # 10KB
                results.append(
                    ValidationResult(
                        category="performance",
                        severity="info",
                        message=f"Large inline CSS: {inline_css_size / 1024:.1f}KB",
                        file_path=str(file_path),
                    )
                )

            inline_js_size = sum(
                len(match)
                for match in re.findall(r"<script[^>]*>(.*?)</script>", content, re.DOTALL)
            )
            if inline_js_size > 10240:  # 10KB
                results.append(
                    ValidationResult(
                        category="performance",
                        severity="info",
                        message=f"Large inline JavaScript: {inline_js_size / 1024:.1f}KB",
                        file_path=str(file_path),
                    )
                )

            # Check for unoptimized images
            img_tags = re.findall(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>', content, re.IGNORECASE)
            for img_src in img_tags:
                if not img_src.startswith("http") and not img_src.startswith("data:"):
                    img_path = file_path.parent / img_src
                    if img_path.exists():
                        img_size = img_path.stat().st_size
                        if img_size > 512 * 1024:  # 512KB
                            results.append(
                                ValidationResult(
                                    category="performance",
                                    severity="info",
                                    message=f"Large image: {img_src} ({img_size / 1024:.1f}KB)",
                                    file_path=str(file_path),
                                )
                            )

        except (OSError, UnicodeDecodeError) as e:
            results.append(
                ValidationResult(
                    category="performance",
                    severity="error",
                    message=f"Failed to validate performance: {e}",
                    file_path=str(file_path),
                )
            )

        return results


class HealthValidator:
    """Main health validation coordinator."""

    def __init__(self, site_dir: Path, base_url: str = ""):
        self.site_dir = site_dir
        self.base_url = base_url
        self.console = Console() if RICH_AVAILABLE else None

        self.html_validator = HTMLValidator()
        self.link_validator = LinkValidator(site_dir, base_url)
        self.seo_validator = SEOValidator()
        self.performance_validator = PerformanceValidator()

    def validate_site(self) -> HealthReport:
        """Validate entire site and return health report."""
        start_time = time.time()

        # Find all HTML files
        html_files = list(self.site_dir.rglob("*.html"))

        all_results = []

        if self.console:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("{task.completed}/{task.total}"),
                console=self.console,
            ) as progress:
                task = progress.add_task("Validating site health...", total=len(html_files))

                for html_file in html_files:
                    # Run all validators
                    all_results.extend(self.html_validator.validate_file(html_file))
                    all_results.extend(self.link_validator.validate_links_in_file(html_file))
                    all_results.extend(self.seo_validator.validate_file(html_file))
                    all_results.extend(self.performance_validator.validate_file(html_file))

                    progress.update(task, advance=1)
        else:
            for i, html_file in enumerate(html_files, 1):
                print(f"Validating {i}/{len(html_files)}: {html_file.name}")

                all_results.extend(self.html_validator.validate_file(html_file))
                all_results.extend(self.link_validator.validate_links_in_file(html_file))
                all_results.extend(self.seo_validator.validate_file(html_file))
                all_results.extend(self.performance_validator.validate_file(html_file))

        # Categorize results
        html_results = [r for r in all_results if r.category == "html"]
        link_results = [r for r in all_results if r.category == "links"]
        accessibility_results = [r for r in all_results if r.category == "accessibility"]
        seo_results = [r for r in all_results if r.category == "seo"]
        performance_results = [r for r in all_results if r.category == "performance"]

        # Calculate scores (0-100)
        html_score = max(0, 100 - len([r for r in html_results if r.severity == "error"]) * 10)
        link_score = max(0, 100 - len([r for r in link_results if r.severity == "error"]) * 10)
        accessibility_score = max(
            0,
            100 - len([r for r in accessibility_results if r.severity in ["error", "warning"]]) * 5,
        )
        seo_score = max(
            0, 100 - len([r for r in seo_results if r.severity in ["error", "warning"]]) * 5
        )
        performance_score = max(
            0, 100 - len([r for r in performance_results if r.severity == "warning"]) * 5
        )

        overall_score = (
            html_score + link_score + accessibility_score + seo_score + performance_score
        ) / 5

        # Count totals
        total_errors = len([r for r in all_results if r.severity == "error"])
        total_warnings = len([r for r in all_results if r.severity == "warning"])

        validation_time = time.time() - start_time

        return HealthReport(
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            total_files_checked=len(html_files),
            total_errors=total_errors,
            total_warnings=total_warnings,
            validation_time_seconds=round(validation_time, 2),
            html_validation_results=html_results,
            link_validation_results=link_results,
            accessibility_results=accessibility_results,
            seo_results=seo_results,
            performance_results=performance_results,
            html_score=round(html_score, 1),
            link_score=round(link_score, 1),
            accessibility_score=round(accessibility_score, 1),
            seo_score=round(seo_score, 1),
            performance_score=round(performance_score, 1),
            overall_score=round(overall_score, 1),
            is_healthy=total_errors == 0 and overall_score >= 80,
        )


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate MkDocs site health")
    parser.add_argument("--site-dir", help="Site directory to validate", default="site", type=Path)
    parser.add_argument("--base-url", help="Base URL for the site", default="")
    parser.add_argument("--strict", help="Fail on warnings", action="store_true")
    parser.add_argument("--output", help="Output JSON report", type=Path)

    args = parser.parse_args()

    if not args.site_dir.exists():
        print(f"❌ Site directory does not exist: {args.site_dir}")
        sys.exit(1)

    # Run validation
    validator = HealthValidator(args.site_dir, args.base_url)
    report = validator.validate_site()

    # Display results
    if RICH_AVAILABLE and validator.console:
        # Rich display
        table = Table(title="Site Health Report")
        table.add_column("Category", style="cyan")
        table.add_column("Score", style="green")
        table.add_column("Errors", style="red")
        table.add_column("Warnings", style="yellow")

        table.add_row(
            "HTML",
            f"{report.html_score}/100",
            str(len([r for r in report.html_validation_results if r.severity == "error"])),
            str(len([r for r in report.html_validation_results if r.severity == "warning"])),
        )
        table.add_row(
            "Links",
            f"{report.link_score}/100",
            str(len([r for r in report.link_validation_results if r.severity == "error"])),
            str(len([r for r in report.link_validation_results if r.severity == "warning"])),
        )
        table.add_row(
            "Accessibility",
            f"{report.accessibility_score}/100",
            str(len([r for r in report.accessibility_results if r.severity == "error"])),
            str(len([r for r in report.accessibility_results if r.severity == "warning"])),
        )
        table.add_row(
            "SEO",
            f"{report.seo_score}/100",
            str(len([r for r in report.seo_results if r.severity == "error"])),
            str(len([r for r in report.seo_results if r.severity == "warning"])),
        )
        table.add_row(
            "Performance",
            f"{report.performance_score}/100",
            str(len([r for r in report.performance_results if r.severity == "error"])),
            str(len([r for r in report.performance_results if r.severity == "warning"])),
        )
        table.add_row(
            "OVERALL",
            f"{report.overall_score}/100",
            str(report.total_errors),
            str(report.total_warnings),
            style="bold",
        )

        validator.console.print(table)

        if report.total_errors > 0 or report.total_warnings > 0:
            validator.console.print("\n[red]Issues Found:[/red]")
            for result in (
                report.html_validation_results
                + report.link_validation_results
                + report.accessibility_results
                + report.seo_results
                + report.performance_results
            ):
                severity_color = {"error": "red", "warning": "yellow", "info": "blue"}[
                    result.severity
                ]
                validator.console.print(
                    f"[{severity_color}]{result.severity.upper()}[/{severity_color}]: "
                    f"{result.message} ({result.file_path})"
                )
    else:
        # Plain text display
        print("✅ Site Health Validation Complete")
        print(f"📄 Files checked: {report.total_files_checked}")
        print(f"⏱️ Validation time: {report.validation_time_seconds}s")
        print(f"🎯 Overall score: {report.overall_score}/100")
        print(f"❌ Errors: {report.total_errors}")
        print(f"⚠️ Warnings: {report.total_warnings}")

        if report.total_errors > 0 or report.total_warnings > 0:
            print("\nIssues found:")
            for result in (
                report.html_validation_results
                + report.link_validation_results
                + report.accessibility_results
                + report.seo_results
                + report.performance_results
            ):
                print(f"{result.severity.upper()}: {result.message} ({result.file_path})")

    # Save JSON report if requested
    if args.output:
        with args.output.open("w") as f:
            json.dump(asdict(report), f, indent=2, default=str)
        print(f"📊 Report saved to: {args.output}")

    # Exit with appropriate code
    if report.total_errors > 0:
        sys.exit(1)
    elif args.strict and report.total_warnings > 0:
        sys.exit(1)
    elif not report.is_healthy:
        print("⚠️ Site health score is below 80")
        sys.exit(1 if args.strict else 0)


if __name__ == "__main__":
    main()
