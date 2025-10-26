#!/usr/bin/env python3
"""Automatically fix frontmatter compliance issues.

This script standardizes frontmatter across all documentation files
by mapping existing tags to approved vocabulary and adding missing fields.
"""

import sys
from pathlib import Path
# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent))

import re
import subprocess
from typing import Dict, List
from datetime import datetime, timezone

import yaml
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from schemas.frontmatter import ALLOWED_TAGS


# Tag mapping for standardization
TAG_MAPPINGS = {
    # Legacy/incorrect tags -> approved tags
    "quality": "validation",
    "pre-commit": "validation",
    "management": "configuration",
    "settings": "configuration",
    "structure": "architecture",
    "services": "docker-compose",
    "stack": "docker-compose",
    "credentials": "authentication",
    "variables": "environment",
    "directories": "architecture",
    "files": "architecture",
    "organization": "architecture",
    "guidelines": "best-practices",
    "principles": "best-practices",
    "execution": "commands",
    "writing-tests": "testing",
    "issues": "troubleshooting",
    "package-manager": "installation",
    "solutions": "alternatives",
    "version-update": "migration",
    "repository": "migration",
    "windows": "setup",
    "pep-585": "python",
    "modernization": "development",
    "errors": "troubleshooting",
    "python-3.14": "python",
    "threat-model": "security",
    "attack-vectors": "security",
    "socket-proxy": "security",
    "policy": "security",
    "socket": "docker",
    "containers": "docker",
    "detection": "monitoring",
    "incident-response": "security",
    "auditing": "security",
    "compliance": "security",
    "hardening": "security",
    "tls": "security",
    "rootless": "docker",
    "alternatives": "reference",
    "requirements": "setup",
    "modules": "python",
    "path-mapping": "migration",
    "reference": "documentation",
    "dry": "utilities",
    "restructure": "migration",
    "powershell": "scripts",
    "linux": "scripts",
    "macos": "scripts",
    "bash": "scripts",
    "components": "architecture",
    "react": "javascript",
    "typescript": "typescript",
    "types": "typescript",
    "state-management": "architecture",
    "hooks": "javascript",
}


def standardize_tags(tags: List[str]) -> List[str]:
    """Standardize tags using mappings and approved vocabulary."""
    standardized = []

    for tag in tags:
        # Direct mapping
        if tag in TAG_MAPPINGS:
            mapped_tag = TAG_MAPPINGS[tag]
            if mapped_tag in ALLOWED_TAGS and mapped_tag not in standardized:
                standardized.append(mapped_tag)
        # Already approved
        elif tag in ALLOWED_TAGS:
            if tag not in standardized:
                standardized.append(tag)
        # Skip unknown tags - they will be replaced with category-appropriate defaults

    # Ensure we have at least one tag
    if not standardized:
        standardized = ["documentation"]

    # Limit to 10 tags max
    return standardized[:10]


def infer_tags_from_path(file_path: Path) -> List[str]:
    """Infer appropriate tags based on file path."""
    path_parts = file_path.parts
    inferred = ["documentation"]  # Default

    # Category-based inference
    if "agent" in path_parts:
        inferred.extend(["agent", "development"])
    elif "api" in path_parts:
        inferred.extend(["api", "reference"])
    elif "production" in path_parts:
        inferred.extend(["production", "deployment"])
    elif "testing" in path_parts:
        inferred.extend(["testing", "pytest"])
    elif "security" in path_parts:
        inferred.extend(["security", "docker"])
    elif "setup" in path_parts:
        inferred.extend(["setup", "installation"])
    elif "scripts" in path_parts:
        inferred.extend(["scripts", "automation"])
    elif "web-content" in path_parts:
        inferred.extend(["web-content", "architecture"])
    elif "readme" in path_parts:
        inferred.extend(["readme", "guide"])
    elif "config" in path_parts:
        inferred.extend(["configuration", "setup"])

    # Technology-based inference
    if "python" in str(file_path).lower():
        inferred.append("python")
    if "docker" in str(file_path).lower():
        inferred.append("docker")
    if "monitoring" in str(file_path).lower():
        inferred.append("monitoring")

    return list(dict.fromkeys(inferred))  # Remove duplicates, preserve order


def fix_frontmatter_content(content: str, file_path: Path) -> str:
    """Fix frontmatter in markdown content."""
    frontmatter_pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if not match:
        # Add missing frontmatter
        now = datetime.now(timezone.utc)
        inferred_tags = infer_tags_from_path(file_path)

        new_frontmatter = f"""---
date_created: "{now.isoformat()}"
last_updated: "{now.isoformat()}"
tags: {inferred_tags}
description: "Documentation for {file_path.stem.replace("-", " ").replace("_", " ")}"
---

"""
        return new_frontmatter + content

    # Parse existing frontmatter
    try:
        frontmatter_data = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        # Invalid YAML, replace entirely
        return fix_frontmatter_content(content[match.end() :], file_path)

    # Fix/add required fields
    now = datetime.now(timezone.utc)

    # Handle dates
    if "date_created" not in frontmatter_data:
        frontmatter_data["date_created"] = now.isoformat()

    if "last_updated" not in frontmatter_data:
        frontmatter_data["last_updated"] = now.isoformat()

    # Fix tags
    existing_tags = frontmatter_data.get("tags", [])
    if isinstance(existing_tags, str):
        existing_tags = [existing_tags]

    standardized_tags = standardize_tags(existing_tags)
    if not standardized_tags:
        standardized_tags = infer_tags_from_path(file_path)

    frontmatter_data["tags"] = standardized_tags

    # Fix description
    if "description" not in frontmatter_data:
        frontmatter_data["description"] = (
            f"Documentation for {file_path.stem.replace('-', ' ').replace('_', ' ')}"
        )
    else:
        desc = frontmatter_data["description"]
        if len(desc) < 20:
            frontmatter_data["description"] = (
                f"{desc} - {file_path.stem.replace('-', ' ').replace('_', ' ')} documentation"
            )
        elif len(desc) > 160:
            frontmatter_data["description"] = desc[:157] + "..."

    # Reconstruct content
    new_frontmatter_yaml = yaml.dump(frontmatter_data, default_flow_style=False, sort_keys=False)
    remaining_content = content[match.end() :]

    return f"---\n{new_frontmatter_yaml}---\n{remaining_content}"


def fix_file(file_path: Path) -> bool:
    """Fix frontmatter in a single file."""
    try:
        original_content = file_path.read_text(encoding="utf-8")
        fixed_content = fix_frontmatter_content(original_content, file_path)

        if original_content != fixed_content:
            file_path.write_text(fixed_content, encoding="utf-8")
            return True
        return False
    except (OSError, yaml.YAMLError, UnicodeDecodeError) as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def fix_all_frontmatter(docs_dir: Path) -> Dict[str, int]:
    """Fix frontmatter in all markdown files."""
    console = Console()
    markdown_files = list(docs_dir.rglob("*.md"))

    stats = {"total": len(markdown_files), "fixed": 0, "errors": 0}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Fixing files...", total=len(markdown_files))

        for file_path in markdown_files:
            relative_path = file_path.relative_to(docs_dir.parent)
            progress.update(task, description=f"Fixing {relative_path.name}")

            try:
                if fix_file(file_path):
                    stats["fixed"] += 1
            except (OSError, yaml.YAMLError, UnicodeDecodeError):
                stats["errors"] += 1

            progress.advance(task)

    return stats


def main() -> None:
    """Main entry point for frontmatter fixing."""
    console = Console()
    docs_dir = Path("docs")

    if not docs_dir.exists():
        console.print("[red]Error: docs directory not found[/red]")
        sys.exit(1)

    console.print("🔧 [bold blue]Fixing frontmatter compliance...[/bold blue]")

    # Run fixes
    stats = fix_all_frontmatter(docs_dir)

    # Report results
    console.print("\\n📊 [bold]Fix Results:[/bold]")
    console.print(f"Total files: {stats['total']}")
    console.print(f"Fixed files: {stats['fixed']}")
    console.print(f"Errors: {stats['errors']}")
    console.print(
        f"Success rate: {((stats['total'] - stats['errors']) / stats['total'] * 100):.1f}%"
    )

    if stats["errors"] == 0:
        console.print("\\n✅ [green]All frontmatter fixed successfully![/green]")

        # Run audit to verify
        console.print("\\n🔍 [blue]Running verification audit...[/blue]")

        result = subprocess.run(
            [sys.executable, ".config/mkdocs/scripts/audit_frontmatter.py"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            console.print("✅ [green]Verification passed! All files are now compliant.[/green]")
        else:
            console.print("⚠️  [yellow]Some issues remain. Check audit output.[/yellow]")

    else:
        console.print(f"\\n⚠️  [yellow]{stats['errors']} files had errors during fixing.[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()
