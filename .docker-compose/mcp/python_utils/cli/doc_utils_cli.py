#!/usr/bin/env python3
"""
CLI entry point for documentation utilities.

Enhanced for Python 3.14 with improved CLI handling.
"""

import argparse
import asyncio
import json
import sys

from .. import has_interpreters
from ..services.doc_utils_service import DocUtils


def main() -> int:
    """Enhanced CLI entry point with Python 3.14 features."""
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
    utils = DocUtils(args.docs_path, use_interpreters=use_interpreters)

    print(f"🐍 Python {sys.version}")
    executor_name = (
        "InterpreterPoolExecutor" if use_interpreters else "ThreadPoolExecutor"
    )
    print(f"🔧 Using {executor_name}")

    results: dict[str, list[str]] = {"valid": [], "broken": [], "skipped": []}

    if args.command == "check-links":
        print("🔗 Checking documentation links...")
        results = utils.check_links_concurrent(max_workers=args.workers)

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

            md_files = utils.find_markdown_files()
            all_links: set[str] = set()
            for file_path in md_files:
                links = utils.extract_links(file_path)
                all_links.update(links)

            results = asyncio.run(
                utils.async_check_links(list(all_links), args.workers)
            )

            print(f"✅ Valid links: {len(results['valid'])}")
            print(f"❌ Broken links: {len(results['broken'])}")
            print(f"⏭️  Skipped links: {len(results['skipped'])}")
        else:
            print("❌ Async checking requires Python 3.14+")

    elif args.command == "inventory":
        print("📦 Generating component inventory...")
        inventory = utils.generate_component_inventory(args.src_path)

        print(f"📄 Pages: {len(inventory['pages'])}")
        print(f"🧩 Components: {len(inventory['components'])}")
        print(f"🪝 Hooks: {len(inventory['hooks'])}")
        print(f"🛠️  Utils: {len(inventory['utils'])}")

        output_file = args.output or "docs/testing/component-inventory.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(inventory, f, indent=2, ensure_ascii=False)

        print(f"📝 Inventory saved to {output_file}")

    if args.output and args.command in ["check-links", "async-check"]:
        results_file = f"{args.output}.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"📊 Results saved to {results_file}")

    return 0


if __name__ == "__main__":
    main()