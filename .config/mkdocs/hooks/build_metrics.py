"""
Build Metrics Collection Hook for MkDocs
========================================

Collects build statistics and metrics during MkDocs build process:
- Build duration
- Page count
- Warning count
- Asset statistics
- Navigation depth

Exports metrics in JSON format for dashboard integration.
Python 3.14 compliant with modern features.

Usage:
    Add to hooks.yml:
    ```yaml
    hooks:
      - .config/mkdocs/hooks/build_metrics.py
    ```

Environment Variables:
    MKDOCS_METRICS_FILE: Output file path (default: site/metrics.json)
    MKDOCS_METRICS_ENABLED: Enable metrics collection (default: true)
"""

import json
import os
import sys
import time
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

# Optional dependency - available when running as MkDocs hook
try:
    import mkdocs

    MKDOCS_VERSION = str(getattr(mkdocs, "__version__", "unknown"))
except ImportError:
    MKDOCS_VERSION = "unknown"


# ============================================================================
# Type Protocols
# ============================================================================


class FilesProtocol(Protocol):
    """Protocol for MkDocs files collection."""

    def __iter__(self) -> Iterator[Any]: ...
    def __len__(self) -> int: ...


class NavProtocol(Protocol):
    """Protocol for MkDocs navigation."""

    pages: list[Any]
    items: list[Any]


# ============================================================================
# Metrics Data Classes
# ============================================================================


@dataclass(frozen=True, slots=True)
class BuildMetrics:
    """Immutable build metrics using Python 3.14 dataclass features."""

    # Build information
    build_timestamp: str
    build_duration_seconds: float
    mkdocs_version: str
    python_version: str

    # Content metrics
    total_pages: int
    markdown_files: int
    static_files: int

    # Navigation metrics
    nav_depth: int
    nav_items: int

    # Asset metrics
    css_files: int
    js_files: int
    image_files: int

    # Build status
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    # Size metrics
    total_size_bytes: int = 0
    largest_page_bytes: int = 0
    largest_page_path: str = ""


@dataclass(slots=True)
class MetricsCollector:
    """Collects and aggregates build metrics during MkDocs build."""

    start_time: float = field(default_factory=time.time)
    enabled: bool = True
    output_file: Path | None = None

    # Counters
    page_count: int = 0
    markdown_count: int = 0
    static_count: int = 0
    css_count: int = 0
    js_count: int = 0
    image_count: int = 0

    # Navigation
    nav_depth: int = 0
    nav_items: int = 0

    # Size tracking
    total_size: int = 0
    largest_page_size: int = 0
    largest_page: str = ""

    # Issues
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def count_file(self, file_path: Path) -> None:
        """Count and categorize a file."""
        suffix = file_path.suffix.lower()

        match suffix:
            case ".md":
                self.markdown_count += 1
            case ".css":
                self.css_count += 1
            case ".js":
                self.js_count += 1
            case ".png" | ".jpg" | ".jpeg" | ".gif" | ".svg" | ".webp":
                self.image_count += 1
            case _:
                self.static_count += 1

        # Track size if file exists
        if file_path.exists():
            try:
                size = file_path.stat().st_size
                self.total_size += size

                if size > self.largest_page_size:
                    self.largest_page_size = size
                    self.largest_page = str(file_path)
            except OSError:
                pass

    def calculate_nav_depth(self, nav_items: list[Any], depth: int = 0) -> int:
        """Recursively calculate navigation depth."""
        max_depth = depth

        for item in nav_items:
            if hasattr(item, "children"):
                child_depth = self.calculate_nav_depth(item.children, depth + 1)
                max_depth = max(max_depth, child_depth)

        return max_depth

    def count_nav_items(self, nav_items: list[Any]) -> int:
        """Recursively count navigation items."""
        count = len(nav_items)

        for item in nav_items:
            if hasattr(item, "children"):
                count += self.count_nav_items(item.children)

        return count

    def create_metrics(self) -> BuildMetrics:
        """Create immutable metrics object."""
        duration = time.time() - self.start_time
        timestamp = datetime.now(UTC).isoformat()
        python_version = (
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )

        return BuildMetrics(
            build_timestamp=timestamp,
            build_duration_seconds=round(duration, 3),
            mkdocs_version=MKDOCS_VERSION,
            python_version=python_version,
            total_pages=self.page_count,
            markdown_files=self.markdown_count,
            static_files=self.static_count,
            nav_depth=self.nav_depth,
            nav_items=self.nav_items,
            css_files=self.css_count,
            js_files=self.js_count,
            image_files=self.image_count,
            warnings=self.warnings.copy(),
            errors=self.errors.copy(),
            total_size_bytes=self.total_size,
            largest_page_bytes=self.largest_page_size,
            largest_page_path=self.largest_page,
        )

    def export_json(self, metrics: BuildMetrics) -> None:
        """Export metrics to JSON file."""
        if not self.enabled or not self.output_file:
            return

        try:
            self.output_file.parent.mkdir(parents=True, exist_ok=True)

            metrics_dict = asdict(metrics)

            with self.output_file.open("w", encoding="utf-8") as f:
                json.dump(metrics_dict, f, indent=2, sort_keys=True, ensure_ascii=False)

            print(f"✅ Build metrics exported to: {self.output_file}")

        except OSError as e:
            print(f"⚠️  Failed to export metrics: {e}")


# ============================================================================
# Singleton Collector Instance
# ============================================================================


class _CollectorRegistry:
    """Registry for singleton metrics collector instance."""

    def __init__(self) -> None:
        self._instance: MetricsCollector | None = None

    def get(self) -> MetricsCollector:
        """Get or create metrics collector instance."""
        if self._instance is None:
            enabled = os.getenv("MKDOCS_METRICS_ENABLED", "true").lower() != "false"
            metrics_file = os.getenv("MKDOCS_METRICS_FILE", "site/metrics.json")

            self._instance = MetricsCollector(
                enabled=enabled, output_file=Path(metrics_file) if enabled else None
            )

        return self._instance


_registry = _CollectorRegistry()


def get_collector() -> MetricsCollector:
    """Get metrics collector instance from registry."""
    return _registry.get()


# ============================================================================
# MkDocs Hooks
# ============================================================================


def on_startup(_command: str, _dirty: bool) -> None:
    """Hook called when MkDocs starts."""
    collector = get_collector()

    if collector.enabled:
        print("📊 Build metrics collection enabled")
        print(f"📁 Metrics output: {collector.output_file}")


def on_files(files: FilesProtocol, config: dict[str, Any]) -> FilesProtocol:
    """Hook called during files collection phase."""
    collector = get_collector()

    if not collector.enabled:
        return files

    docs_dir = Path(config.get("docs_dir", "docs"))

    for file in files:
        collector.page_count += 1
        file_path = docs_dir / file.src_path
        collector.count_file(file_path)

    return files


def on_nav(nav: NavProtocol, _config: dict[str, Any], _files: FilesProtocol) -> NavProtocol:
    """Hook called after navigation is constructed."""
    collector = get_collector()

    if not collector.enabled:
        return nav

    if hasattr(nav, "items"):
        collector.nav_depth = collector.calculate_nav_depth(nav.items)
        collector.nav_items = collector.count_nav_items(nav.items)
    elif hasattr(nav, "pages"):
        collector.nav_items = len(nav.pages)
        collector.nav_depth = 1

    return nav


def on_post_build(_config: dict[str, Any]) -> None:
    """Hook called after the build completes."""
    collector = get_collector()

    if not collector.enabled:
        return

    # Create and export metrics
    metrics = collector.create_metrics()
    collector.export_json(metrics)

    # Print summary to stdout (structured logging)
    print("\n" + "=" * 80)
    print("BUILD METRICS SUMMARY")
    print("=" * 80)
    print(f"Duration: {metrics.build_duration_seconds}s")
    print(f"Total Pages: {metrics.total_pages}")
    print(f"Markdown Files: {metrics.markdown_files}")
    print(f"Navigation Depth: {metrics.nav_depth}")
    print(f"Navigation Items: {metrics.nav_items}")
    print(f"Total Size: {metrics.total_size_bytes / 1024 / 1024:.2f} MB")

    if metrics.warnings:
        print(f"Warnings: {len(metrics.warnings)}")
    if metrics.errors:
        print(f"Errors: {len(metrics.errors)}")

    print("=" * 80 + "\n")
