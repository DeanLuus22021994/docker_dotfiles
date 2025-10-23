"""
Command-line interface for React Scuba utilities.

This module provides the CLI entry point with support for all
documentation utilities and services.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from ..config.settings import HTTPConfig, PathConfig, get_python_features
from ..models.models import ComponentInventoryConfig, LinkCheckConfig
from ..services.component_inventory import ComponentInventoryService
from ..services.link_checker import LinkCheckerService


def main() -> int:
    """Enhanced CLI entry point with Python 3.14 features."""
    parser = argparse.ArgumentParser(
        description="React Scuba Documentation Utilities (Python 3.14 Enhanced)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  react-scuba-utils check-links
  react-scuba-utils inventory --src-path src
  react-scuba-utils check-links --workers 20

Python 3.14 Features:
  - Free-threaded execution for true parallelism
  - Concurrent interpreters for isolated processing
  - Enhanced pathlib operations
  - Improved concurrent.futures support
        """,
    )

    parser.add_argument(
        "command",
        choices=["check-links", "inventory", "async-check"],
        help="Command to run",
    )
    parser.add_argument("--docs-path", default="docs", help="Path to docs directory")
    parser.add_argument("--src-path", default="src", help="Path to source directory")
    parser.add_argument(
        "--workers", type=int, default=10, help="Number of worker threads/interpreters"
    )
    parser.add_argument(
        "--timeout", type=int, default=10, help="HTTP request timeout in seconds"
    )
    parser.add_argument(
        "--no-interpreters",
        action="store_true",
        help="Disable concurrent interpreters (use threads only)",
    )
    parser.add_argument("--output", help="Output file for results")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    # Display Python version and features
    features = get_python_features()
    print(f"🐍 Python {features['version_string']}")
    if features["is_free_threaded"]:
        print("🧵 Running in free-threaded mode")
    if features["has_interpreters"]:
        print("🔄 Concurrent interpreters available")

    # Initialize configurations
    path_config = PathConfig(
        docs_path=Path(args.docs_path), src_path=Path(args.src_path)
    )
    http_config = HTTPConfig(timeout=args.timeout)
    use_interpreters = not args.no_interpreters and features["has_interpreters"]

    executor_name = (
        "InterpreterPoolExecutor" if use_interpreters else "ThreadPoolExecutor"
    )
    print(f"🔧 Using {executor_name}")

    # Execute command
    if args.command == "check-links":
        _run_link_check(args, path_config, http_config, use_interpreters)
    elif args.command == "async-check":
        _run_async_link_check(args, path_config, http_config)
    elif args.command == "inventory":
        _run_inventory(args, path_config)

    return 0


def _run_link_check(
    args: argparse.Namespace,
    path_config: PathConfig,
    http_config: HTTPConfig,
    use_interpreters: bool,
) -> None:
    """Run synchronous link checking."""
    print("🔗 Checking documentation links...")

    config = LinkCheckConfig(
        max_workers=args.workers,
        timeout=args.timeout,
        use_interpreters=use_interpreters,
    )

    service = LinkCheckerService(config, path_config, http_config)
    results = service.check_links_concurrent()

    _display_link_results(results, args.output, args.json)


def _run_async_link_check(
    args: argparse.Namespace, path_config: PathConfig, http_config: HTTPConfig
) -> None:
    """Run asynchronous link checking."""
    if sys.version_info < (3, 14):
        print("❌ Async checking requires Python 3.14+")
        sys.exit(1)

    print("🔗 Checking links asynchronously (Python 3.14 free-threaded)...")

    config = LinkCheckConfig(
        max_workers=args.workers,
        timeout=args.timeout,
        use_interpreters=False,  # Async uses asyncio instead
    )

    service = LinkCheckerService(config, path_config, http_config)

    # Get all links first
    md_files = service.find_markdown_files()
    all_links = set()
    for file_path in md_files:
        links = service.extract_links(file_path)
        all_links.update(links)

    # Run async check
    results = asyncio.run(service.async_check_links(list(all_links)))

    _display_link_results(results, args.output, args.json)


def _run_inventory(args: argparse.Namespace, path_config: PathConfig) -> None:
    """Run component inventory generation."""
    print("📦 Generating component inventory...")

    config = ComponentInventoryConfig(src_path=args.src_path)
    service = ComponentInventoryService(config, path_config)
    inventory = service.generate_inventory()

    # Display summary
    print(f"📄 Pages: {len(inventory['pages'])}")
    print(f"🧩 Components: {len(inventory['components'])}")
    print(f"🪝 Hooks: {len(inventory['hooks'])}")
    print(f"🛠️  Utils: {len(inventory['utils'])}")

    # Save to JSON
    output_file = args.output or "docs/testing/component-inventory.json"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)

    print(f"📝 Inventory saved to {output_file}")


def _display_link_results(
    results: dict[str, list[str]],
    output_file: str | None = None,
    json_output: bool = False,
) -> None:
    """Display link check results."""
    print(f"✅ Valid links: {len(results['valid'])}")
    print(f"❌ Broken links: {len(results['broken'])}")
    print(f"⏭️  Skipped links: {len(results['skipped'])}")

    if results["broken"]:
        print("\n❌ Broken links:")
        for link in results["broken"][:10]:  # Show first 10
            print(f"  - {link}")
        if len(results["broken"]) > 10:
            print(f"  ... and {len(results['broken']) - 10} more")

    # Save results if requested
    if output_file:
        results_file = f"{output_file}.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"📊 Results saved to {results_file}")

    # JSON output mode
    if json_output:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
