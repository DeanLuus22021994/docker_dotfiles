#!/usr/bin/env python3
"""Document template generator with interactive CLI.

Usage:
    python .config/mkdocs/scripts/new_doc.py
    python .config/mkdocs/scripts/new_doc.py --category readme --title "Setup Guide"
"""

import argparse
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, TYPE_CHECKING, cast

# Handle optional dependencies gracefully
try:
    import jinja2

    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    print("Warning: Jinja2 not available. Template rendering disabled.")

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("Warning: PyYAML not available. .pages file updates disabled.")

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm, Prompt

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

    # Fallback implementations with unique names
    class FallbackConsole:
        """Fallback console implementation."""

        def print(self, *args: object, **_kwargs: object) -> None:
            """Print to console."""
            print(*args)

    class FallbackProgress:
        """Fallback progress implementation."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Initialize progress."""

        def __enter__(self) -> "FallbackProgress":
            """Enter context."""
            return self

        def __exit__(self, *args: Any) -> None:
            """Exit context."""

        def add_task(self, **kwargs: Any) -> None:
            """Add task."""

    class FallbackConfirm:
        """Fallback confirm implementation."""

        @staticmethod
        def ask(question: str) -> bool:
            """Ask for confirmation."""
            response = input(f"{question} (y/N): ").strip().lower()
            return response in ("y", "yes")

    class FallbackPrompt:
        """Fallback prompt implementation."""

        @staticmethod
        def ask(question: str, default: str = "") -> str:
            """Ask for input."""
            response = input(f"{question} [{default}]: ").strip()
            return response if response else default

    # Use fallback classes directly
    globals()["Console"] = FallbackConsole
    globals()["Progress"] = FallbackProgress
    globals()["Confirm"] = FallbackConfirm
    globals()["Prompt"] = FallbackPrompt


# Add the parent directory to sys.path for imports
# sys.path.append(str(Path(__file__).parent.parent))  # Not needed with relative import

if TYPE_CHECKING:
    from ..schemas.frontmatter import DocFrontmatter as _DocFrontmatterType
else:

    class _DocFrontmatterType:  # pragma: no cover - typing helper
        """Minimal signature placeholder for DocFrontmatter."""

        def __init__(self, **_: Any) -> None: ...


_RuntimeDocFrontmatter: Any
try:
    from ..schemas.frontmatter import DocFrontmatter as _RuntimeDocFrontmatter
except ImportError:
    # Fallback if schemas not available
    @dataclass
    class _FallbackDocFrontmatter:
        """Fallback frontmatter dataclass when Pydantic is not available."""

        title: str
        date_created: datetime
        last_updated: datetime
        tags: list[str]
        description: str

    _RuntimeDocFrontmatter = _FallbackDocFrontmatter


def _build_frontmatter(**kwargs: Any) -> _DocFrontmatterType:
    """Create a frontmatter instance using the available implementation."""

    return cast(_DocFrontmatterType, _RuntimeDocFrontmatter(**kwargs))


DOC_FRONTMATTER_FACTORY: Callable[..., _DocFrontmatterType] = _build_frontmatter


@dataclass(frozen=True, slots=True)
class DocCategory:
    """Document category configuration."""

    name: str
    path: Path
    template: str
    description: str


# Available document categories
CATEGORIES: list[DocCategory] = [
    DocCategory("readme", Path("docs/readme"), "readme.j2", "Getting started documentation"),
    DocCategory("agent", Path("docs/agent"), "agent.j2", "AI agent development guides"),
    DocCategory("api", Path("docs/api"), "api.j2", "API reference documentation"),
    DocCategory("index", Path("docs/index"), "index.j2", "Index and overview pages"),
    DocCategory("config", Path("docs/config"), "base.j2", "Configuration documentation"),
    DocCategory("production", Path("docs/production"), "base.j2", "Production deployment guides"),
    DocCategory("testing", Path("docs/testing"), "base.j2", "Testing documentation"),
    DocCategory("security", Path("docs/security"), "base.j2", "Security documentation"),
]

ALLOWED_TAGS = {
    # Core categories
    "docker",
    "platform",
    "index",
    "documentation",
    "readme",
    "agent",
    "api",
    "setup",
    "guide",
    # Technical areas
    "configuration",
    "deployment",
    "development",
    "testing",
    "monitoring",
    "security",
    "networking",
    "storage",
    # Languages/Tools
    "python",
    "javascript",
    "typescript",
    "golang",
    "terraform",
    "ansible",
    "kubernetes",
    "compose",
    # Patterns
    "tutorial",
    "reference",
    "howto",
    "explanation",
    "troubleshooting",
    "best-practices",
    "architecture",
}


def get_template_env() -> Any:  # Returns jinja2.Environment when available
    """Create Jinja2 environment for template rendering."""
    if not JINJA2_AVAILABLE:
        raise RuntimeError("Jinja2 is required for template rendering")

    template_dir = Path(__file__).parent.parent / "templates"
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=jinja2.select_autoescape(["html", "xml"]),
    )


def interactive_prompt(console: Any) -> tuple[str, str, Any]:
    """Run interactive CLI prompts for doc creation."""
    console.print("🚀 [bold blue]MkDocs Document Generator[/bold blue]")
    console.print("Create new documentation with validated frontmatter\\n")

    # Category selection
    console.print("[bold]Available Categories:[/bold]")
    for i, category in enumerate(CATEGORIES, 1):
        console.print(f"  {i}. [cyan]{category.name}[/cyan] - {category.description}")

    while True:
        try:
            choice = int(Prompt.ask("\\nSelect category", default="1")) - 1
            if 0 <= choice < len(CATEGORIES):
                selected_category = CATEGORIES[choice]
                break
            else:
                console.print("[red]Invalid choice. Please try again.[/red]")
        except ValueError:
            console.print("[red]Please enter a number.[/red]")

    # Document details
    title = Prompt.ask(
        "\\nDocument title", default=f"New {selected_category.name.title()} Document"
    )

    description = ""
    while len(description) < 20 or len(description) > 160:
        description = Prompt.ask(
            "Brief description (20-160 characters)", default=f"Documentation for {title.lower()}"
        )
        if len(description) < 20:
            console.print("[red]Description too short (minimum 20 characters)[/red]")
        elif len(description) > 160:
            console.print("[red]Description too long (maximum 160 characters)[/red]")

    # Tag selection
    console.print("\\n[bold]Available Tags:[/bold]")
    tag_list = sorted(ALLOWED_TAGS)
    for i, tag in enumerate(tag_list, 1):
        console.print(f"  {i:2d}. {tag}")

    console.print("\\nEnter tag numbers separated by spaces (e.g., 1 5 12)")
    suggested_tags = [selected_category.name, "documentation"]
    console.print(f"Suggested: [cyan]{', '.join(suggested_tags)}[/cyan]")

    tag_input = Prompt.ask("Tag numbers", default="")

    if tag_input.strip():
        try:
            tag_indices = [int(x.strip()) - 1 for x in tag_input.split()]
            selected_tags = [tag_list[i] for i in tag_indices if 0 <= i < len(tag_list)]
        except (ValueError, IndexError):
            console.print("[yellow]Invalid tag selection, using suggested tags[/yellow]")
            selected_tags = suggested_tags
    else:
        selected_tags = suggested_tags

    # Create frontmatter with validation
    now = datetime.now(timezone.utc)
    frontmatter = DOC_FRONTMATTER_FACTORY(
        title=title,
        date_created=now,
        last_updated=now,
        tags=selected_tags,
        description=description,
    )

    return selected_category.name, title, frontmatter


def update_pages_file(category_path: Path, filename: str, title: str) -> None:
    """Update .pages file with new document entry."""
    if not YAML_AVAILABLE:
        print("Warning: PyYAML not available. Skipping .pages file update.")
        return

    pages_file = category_path / ".pages"

    if pages_file.exists():
        with open(pages_file, "r", encoding="utf-8") as f:
            try:
                pages = yaml.safe_load(f) or {}
            except yaml.YAMLError:
                pages = {}
    else:
        pages = {"nav": []}

    if "nav" not in pages:
        pages["nav"] = []

    # Add new entry if not already present
    nav_entry = {title: filename}
    if nav_entry not in pages["nav"]:
        pages["nav"].append(nav_entry)

        # Write updated .pages file
        with open(pages_file, "w", encoding="utf-8") as f:
            yaml.dump(pages, f, default_flow_style=False, sort_keys=False)


def create_document(category: str, title: str, frontmatter: Any, console: Any) -> Path:
    """Create new document with template and frontmatter."""

    # Find category config
    category_config = next((c for c in CATEGORIES if c.name == category), None)
    if not category_config:
        raise ValueError(f"Unknown category: {category}")

    # Ensure category directory exists
    category_config.path.mkdir(parents=True, exist_ok=True)

    # Generate filename from title
    filename = title.lower().replace(" ", "-").replace("_", "-")
    filename = "".join(c for c in filename if c.isalnum() or c in "-")
    filename = f"{filename}.md"

    file_path = category_config.path / filename

    # Check if file exists
    if file_path.exists():
        if not Confirm.ask(f"File {file_path} already exists. Overwrite?"):
            console.print("[yellow]Operation cancelled.[/yellow]")
            return file_path

    # Render template
    env = get_template_env()
    template = env.get_template(category_config.template)

    content = template.render(
        title=title,
        description=frontmatter.description,
        date_created=frontmatter.date_created,
        last_updated=frontmatter.last_updated,
        tags=frontmatter.tags,
    )

    # Write file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Update .pages file for navigation
    update_pages_file(category_config.path, filename, title)

    return file_path


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate new MkDocs documentation")
    parser.add_argument(
        "--category", choices=[c.name for c in CATEGORIES], help="Document category"
    )
    parser.add_argument("--title", help="Document title")
    parser.add_argument("--description", help="Document description")
    parser.add_argument("--tags", nargs="+", help="Document tags")
    parser.add_argument(
        "--non-interactive", action="store_true", help="Run without interactive prompts"
    )

    args = parser.parse_args()
    console = Console()

    try:
        if args.non_interactive and all([args.category, args.title, args.description]):
            # Non-interactive mode
            now = datetime.now(timezone.utc)
            frontmatter = DOC_FRONTMATTER_FACTORY(
                title=args.title,
                date_created=now,
                last_updated=now,
                tags=args.tags or [args.category, "documentation"],
                description=args.description,
            )

            category = args.category
            title = args.title
        else:
            # Interactive mode
            category, title, frontmatter = interactive_prompt(console)

        # Create document with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Creating document...", total=None)
            file_path = create_document(category, title, frontmatter, console)

        console.print("\\n✅ [green]Document created successfully![/green]")
        console.print(f"📄 File: [cyan]{file_path}[/cyan]")
        console.print(f"📁 Category: [cyan]{category}[/cyan]")
        console.print(f"🏷️  Tags: [cyan]{', '.join(frontmatter.tags)}[/cyan]")

    except KeyboardInterrupt:
        console.print("\\n[yellow]Operation cancelled by user.[/yellow]")
        sys.exit(1)
    except (ValueError, RuntimeError, OSError) as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
