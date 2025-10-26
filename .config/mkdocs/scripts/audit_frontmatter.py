#!/usr/bin/env python3
"""Audit existing documentation for frontmatter compliance.

This script scans all markdown files in the docs directory and reports
frontmatter compliance issues according to the DocFrontmatter schema.
"""

import sys

import re
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path

import yaml
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from ..schemas.frontmatter import ALLOWED_TAGS


@dataclass
class FrontmatterIssue:
    """Represents a frontmatter validation issue."""

    file_path: Path
    issue_type: str
    description: str
    suggested_fix: Optional[str] = None


@dataclass
class AuditResult:
    """Results of frontmatter audit."""

    total_files: int
    compliant_files: int
    issues: List[FrontmatterIssue]

    @property
    def compliance_rate(self) -> float:
        """Calculate compliance rate as percentage."""
        if self.total_files == 0:
            return 100.0
        return (self.compliant_files / self.total_files) * 100


def extract_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter from markdown content."""
    frontmatter_pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if not match:
        return None

    try:
        result = yaml.safe_load(match.group(1))
        return result if isinstance(result, dict) else None
    except yaml.YAMLError:
        return None


def validate_frontmatter(file_path: Path, frontmatter: dict[str, Any]) -> list[FrontmatterIssue]:
    """Validate frontmatter against DocFrontmatter schema."""
    issues = []

    # Check required fields
    required_fields = ["date_created", "last_updated", "tags", "description"]
    for field in required_fields:
        if field not in frontmatter:
            issues.append(
                FrontmatterIssue(
                    file_path=file_path,
                    issue_type="missing_field",
                    description=f"Missing required field: {field}",
                    suggested_fix=f"Add {field} to frontmatter",
                )
            )

    # Validate date fields
    for date_field in ["date_created", "last_updated"]:
        if date_field in frontmatter:
            date_value = frontmatter[date_field]
            if not isinstance(date_value, str):
                issues.append(
                    FrontmatterIssue(
                        file_path=file_path,
                        issue_type="invalid_date_format",
                        description=f"{date_field} must be ISO 8601 string",
                        suggested_fix=f"Use format: {datetime.now(timezone.utc).isoformat()}",
                    )
                )
            else:
                try:
                    datetime.fromisoformat(date_value.replace("Z", "+00:00"))
                except ValueError:
                    issues.append(
                        FrontmatterIssue(
                            file_path=file_path,
                            issue_type="invalid_date_value",
                            description=f"{date_field} has invalid ISO 8601 format",
                            suggested_fix="Use ISO 8601 format with timezone",
                        )
                    )

    # Validate tags
    if "tags" in frontmatter:
        tags = frontmatter["tags"]
        if not isinstance(tags, list):
            issues.append(
                FrontmatterIssue(
                    file_path=file_path,
                    issue_type="invalid_tags_type",
                    description="Tags must be a list",
                    suggested_fix='Convert tags to list format: ["tag1", "tag2"]',
                )
            )
        elif len(tags) == 0:
            issues.append(
                FrontmatterIssue(
                    file_path=file_path,
                    issue_type="empty_tags",
                    description="Tags list cannot be empty",
                    suggested_fix="Add at least one relevant tag",
                )
            )
        elif len(tags) > 10:
            issues.append(
                FrontmatterIssue(
                    file_path=file_path,
                    issue_type="too_many_tags",
                    description=f"Too many tags ({len(tags)}/10 max)",
                    suggested_fix="Reduce to maximum 10 most relevant tags",
                )
            )
        else:
            # Check for invalid tags
            invalid_tags = set(tags) - ALLOWED_TAGS
            if invalid_tags:
                issues.append(
                    FrontmatterIssue(
                        file_path=file_path,
                        issue_type="invalid_tags",
                        description=f"Invalid tags: {sorted(invalid_tags)}",
                        suggested_fix=f"Use allowed tags: {sorted(ALLOWED_TAGS)}",
                    )
                )

    # Validate description
    if "description" in frontmatter:
        description = frontmatter["description"]
        if not isinstance(description, str):
            issues.append(
                FrontmatterIssue(
                    file_path=file_path,
                    issue_type="invalid_description_type",
                    description="Description must be a string",
                    suggested_fix="Convert description to string",
                )
            )
        elif len(description) < 20:
            issues.append(
                FrontmatterIssue(
                    file_path=file_path,
                    issue_type="description_too_short",
                    description=f"Description too short ({len(description)}/20 min)",
                    suggested_fix="Expand description to at least 20 characters",
                )
            )
        elif len(description) > 160:
            issues.append(
                FrontmatterIssue(
                    file_path=file_path,
                    issue_type="description_too_long",
                    description=f"Description too long ({len(description)}/160 max)",
                    suggested_fix="Shorten description to maximum 160 characters",
                )
            )

    return issues


def audit_file(file_path: Path) -> List[FrontmatterIssue]:
    """Audit a single markdown file for frontmatter compliance."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return [
            FrontmatterIssue(
                file_path=file_path,
                issue_type="file_read_error",
                description=f"Cannot read file: {e}",
                suggested_fix="Check file encoding and permissions",
            )
        ]

    frontmatter = extract_frontmatter(content)
    if frontmatter is None:
        return [
            FrontmatterIssue(
                file_path=file_path,
                issue_type="missing_frontmatter",
                description="No valid YAML frontmatter found",
                suggested_fix="Add frontmatter with --- delimiters",
            )
        ]

    return validate_frontmatter(file_path, frontmatter)


def audit_documentation(docs_dir: Path) -> AuditResult:
    """Audit all markdown files in the docs directory."""
    console = Console()
    markdown_files = list(docs_dir.rglob("*.md"))

    all_issues = []
    compliant_files = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Auditing files...", total=len(markdown_files))

        for file_path in markdown_files:
            relative_path = file_path.relative_to(docs_dir.parent)
            progress.update(task, description=f"Auditing {relative_path.name}")

            issues = audit_file(file_path)
            if issues:
                all_issues.extend(issues)
            else:
                compliant_files += 1

            progress.advance(task)

    return AuditResult(
        total_files=len(markdown_files), compliant_files=compliant_files, issues=all_issues
    )


def generate_report(result: AuditResult, output_file: Optional[Path] = None) -> None:
    """Generate detailed audit report."""
    console = Console()

    # Summary statistics
    console.print("\\n📊 [bold blue]Frontmatter Audit Report[/bold blue]")
    console.print(f"Total files audited: {result.total_files}")
    console.print(f"Compliant files: {result.compliant_files}")
    console.print(f"Files with issues: {len(result.issues)}")
    console.print(f"Compliance rate: {result.compliance_rate:.1f}%")

    if not result.issues:
        console.print("\\n🎉 [green]All files are compliant![/green]")
        return

    # Group issues by type
    issues_by_type: dict[str, list[FrontmatterIssue]] = {}
    for issue in result.issues:
        if issue.issue_type not in issues_by_type:
            issues_by_type[issue.issue_type] = []
        issues_by_type[issue.issue_type].append(issue)

    # Issue type summary
    console.print("\\n📋 [bold]Issue Summary by Type[/bold]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Issue Type", style="cyan")
    table.add_column("Count", justify="right", style="red")

    for issue_type, issues in sorted(issues_by_type.items()):
        table.add_row(issue_type.replace("_", " ").title(), str(len(issues)))

    console.print(table)

    # Detailed issues
    console.print("\\n🔍 [bold]Detailed Issues[/bold]")
    for issue_type, issues in sorted(issues_by_type.items()):
        console.print(f"\\n[bold yellow]{issue_type.replace('_', ' ').title()}:[/bold yellow]")
        for issue in issues[:5]:  # Show first 5 of each type
            try:
                rel_path = issue.file_path.relative_to(Path.cwd())
            except ValueError:
                rel_path = issue.file_path
            console.print(f"  • {rel_path}: {issue.description}")
            if issue.suggested_fix:
                console.print(f"    💡 Fix: {issue.suggested_fix}")

        if len(issues) > 5:
            console.print(f"    ... and {len(issues) - 5} more files")

    # Save report to file if requested
    if output_file:
        report_content = generate_markdown_report(result)
        output_file.write_text(report_content, encoding="utf-8")
        console.print(f"\\n📝 Report saved to: {output_file}")


def generate_markdown_report(result: AuditResult) -> str:
    """Generate markdown format report."""
    lines = [
        "# Frontmatter Audit Report",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        f"**Total Files:** {result.total_files}",
        f"**Compliant Files:** {result.compliant_files}",
        f"**Files with Issues:** {len(set(issue.file_path for issue in result.issues))}",
        f"**Compliance Rate:** {result.compliance_rate:.1f}%",
        "",
        "## Issues by File",
        "",
    ]

    # Group by file
    issues_by_file: dict[Path, list[FrontmatterIssue]] = {}
    for issue in result.issues:
        if issue.file_path not in issues_by_file:
            issues_by_file[issue.file_path] = []
        issues_by_file[issue.file_path].append(issue)

    for file_path, file_issues in sorted(issues_by_file.items()):
        rel_path = file_path.relative_to(Path.cwd())
        lines.append(f"### `{rel_path}`")
        lines.append("")

        for issue in file_issues:
            lines.append(f"- **{issue.issue_type.replace('_', ' ').title()}**: {issue.description}")
            if issue.suggested_fix:
                lines.append(f"  - 💡 **Fix**: {issue.suggested_fix}")

        lines.append("")

    return "\\n".join(lines)


def main() -> None:
    """Main entry point for frontmatter audit."""
    console = Console()
    docs_dir = Path("docs")

    if not docs_dir.exists():
        console.print("[red]Error: docs directory not found[/red]")
        sys.exit(1)

    console.print("🔍 [bold blue]Starting frontmatter audit...[/bold blue]")

    result = audit_documentation(docs_dir)

    # Generate report
    report_file = Path(".config/mkdocs/frontmatter-audit.md")
    generate_report(result, report_file)

    # Exit with appropriate code
    if result.compliance_rate < 100:
        console.print(
            "\\n⚠️  [yellow]Audit completed with issues. "
            "Run fixes before enabling strict mode.[/yellow]"
        )
        sys.exit(1)
    else:
        console.print("\\n✅ [green]All files are compliant! Ready for strict mode.[/green]")
        sys.exit(0)


if __name__ == "__main__":
    main()
