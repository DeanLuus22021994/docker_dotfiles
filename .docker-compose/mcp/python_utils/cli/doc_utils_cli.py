#!/usr/bin/env python3
"""
CLI entry point for documentation utilities.

Enhanced for Python 3.14 with improved CLI handling.
Uses the existing docker_examples_utils services for consistency.

This module provides a command-line interface for various documentation
utilities including link checking and component inventory generation.
It leverages Python 3.14+ features when available for enhanced performance.
"""

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

from docker_examples_utils.config.settings import (
    HTTPConfig,
    PathConfig,
    has_interpreters,
)
from docker_examples_utils.models.models import (
    ComponentInventoryConfig,
    LinkCheckConfig,
)
from docker_examples_utils.services.component_inventory import (
    ComponentInventoryService,
)
from docker_examples_utils.services.link_checker import LinkCheckerService


def main() -> int:
    """
    Enhanced CLI entry point with Python 3.14 features.

    This function provides a command-line interface for documentation utilities,
    supporting link checking, component inventory generation, and async operations.
    It automatically detects and utilizes Python 3.14+ features when available.

    Commands:
        check-links: Validate all links in documentation files
        inventory: Generate component inventory from source files
        async-check: Asynchronous link checking (Python 3.14+ required)

    Returns:
        int: Exit code (0 for success, non-zero for errors)

    Raises:
        KeyboardInterrupt: When operation is cancelled by user
        Exception: For unexpected errors during execution
    """
    try:
        parser = argparse.ArgumentParser(
            description="Docker Compose Documentation Utilities (Python 3.14 Enhanced)",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python -m python_utils.cli.doc_utils_cli check-links
  python -m python_utils.cli.doc_utils_cli inventory --src-path src
  python -m python_utils.cli.doc_utils_cli check-links --workers 20

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
            "--no-interpreters",
            action="store_true",
            help="Disable concurrent interpreters (use threads only)",
        )
        parser.add_argument("--output", help="Output file for results")

        args = parser.parse_args()

        use_interpreters = not args.no_interpreters and has_interpreters()
        path_config = PathConfig()
        http_config = HTTPConfig()

        print(f"🐍 Python {sys.version}")
        executor_name = (
            "InterpreterPoolExecutor" if use_interpreters else "ThreadPoolExecutor"
        )
        print(f"🔧 Using {executor_name}")

        results: dict[str, list[str]] = {"valid": [], "broken": [], "skipped": []}

        if args.command == "check-links":
            print("🔗 Checking documentation links...")
            config = LinkCheckConfig(
                max_workers=args.workers,
                timeout=10,
                use_interpreters=use_interpreters,
            )
            service = LinkCheckerService(config, path_config, http_config)
            results = service.check_links_concurrent()

            print(f"✅ Valid links: {len(results['valid'])}")
            print(f"❌ Broken links: {len(results['broken'])}")
            print(f"⏭️  Skipped links: {len(results['skipped'])}")

            if results["broken"]:
                print("\n❌ Broken links:")
                for link in results["broken"][:10]:
                    print(f"  - {link}")
                if len(results["broken"]) > 10:
                    print(f"  ... and {len(results['broken']) - 10} more")

        elif args.command == "async-check":
            if sys.version_info >= (3, 14):
                print("🔗 Checking links asynchronously (Python 3.14 free-threaded)...")
                config = LinkCheckConfig(
                    max_workers=args.workers,
                    timeout=10,
                    use_interpreters=use_interpreters,
                )
                service = LinkCheckerService(config, path_config, http_config)
                
                # Collect all links from documentation files
                all_links: set[str] = set()
                docs_path = Path(args.docs_path)
                if docs_path.exists():
                    for md_file in docs_path.rglob("*.md"):
                        try:
                            content = md_file.read_text(encoding="utf-8")
                            # Simple link extraction (could be improved)
                            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                            for _, url in links:
                                if not url.startswith(("http://", "https://", "#")):
                                    all_links.add(url)
                                elif url.startswith(("http://", "https://")):
                                    all_links.add(url)
                        except Exception:
                            pass
                
                results = asyncio.run(service.async_check_links(list(all_links)))

                print(f"✅ Valid links: {len(results['valid'])}")
                print(f"❌ Broken links: {len(results['broken'])}")
                print(f"⏭️  Skipped links: {len(results['skipped'])}")
            else:
                print("❌ Async checking requires Python 3.14+")

        elif args.command == "inventory":
            print("📦 Generating component inventory...")
            config = ComponentInventoryConfig(src_path=args.src_path)
            service = ComponentInventoryService(config, path_config)
            inventory = service.generate_inventory()

            print(f"📄 Pages: {len(inventory.get('pages', []))}")
            print(f"🧩 Components: {len(inventory.get('components', []))}")
            print(f"🪝 Hooks: {len(inventory.get('hooks', []))}")
            print(f"🛠️  Utils: {len(inventory.get('utils', []))}")

            if args.output:
                output_file = args.output if args.output.endswith('.json') else f"{args.output}.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(inventory, f, indent=2, ensure_ascii=False)
                print(f"📝 Inventory saved to {output_file}")
            else:
                # Default behavior - save to docs/testing/component-inventory.json if docs directory exists
                default_output = "docs/testing/component-inventory.json"
                try:
                    with open(default_output, "w", encoding="utf-8") as f:
                        json.dump(inventory, f, indent=2, ensure_ascii=False)
                    print(f"📝 Inventory saved to {default_output}")
                except (OSError, IOError):
                    # If we can't write to the default location, just continue without saving
                    pass

        if args.output and args.command in ["check-links", "async-check"]:
            results_file = args.output if args.output.endswith('.json') else f"{args.output}.json"
            with open(results_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"📊 Results saved to {results_file}")

        return 0

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    main()