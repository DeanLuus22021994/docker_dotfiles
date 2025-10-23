"""
Core module for React Scuba utilities.

This module provides the main DocUtils class that orchestrates
all documentation utilities and services.
"""

from pathlib import Path
from typing import Any

from ..config.settings import HTTPConfig, PathConfig
from ..models.models import ComponentInventoryConfig, LinkCheckConfig
from ..services.component_inventory import ComponentInventoryService
from ..services.file_operations import FileOperationsService
from ..services.link_checker import LinkCheckerService


class DocUtils:
    """
    Enhanced documentation utilities leveraging Python 3.14 features.

    This is the main orchestration class that provides a unified interface
    to all documentation utilities and services.
    """

    def __init__(
        self,
        docs_path: str = "docs",
        src_path: str = "src",
        use_interpreters: bool = True,
    ):
        """
        Initialize DocUtils with configuration.

        Args:
            docs_path: Path to documentation directory
            src_path: Path to source directory
            use_interpreters: Whether to use concurrent interpreters
        """
        self.path_config = PathConfig(
            docs_path=Path(docs_path), src_path=Path(src_path)
        )
        self.http_config = HTTPConfig()

        # Initialize service configurations
        self.link_config = LinkCheckConfig(use_interpreters=use_interpreters)
        self.inventory_config = ComponentInventoryConfig(src_path=src_path)

        # Initialize services
        self.link_checker = LinkCheckerService(
            self.link_config, self.path_config, self.http_config
        )
        self.component_inventory = ComponentInventoryService(
            self.inventory_config, self.path_config
        )
        self.file_operations = FileOperationsService()

    def check_links_concurrent(self, max_workers: int = 10) -> dict[str, list[str]]:
        """
        Check all documentation links concurrently.

        Args:
            max_workers: Maximum number of concurrent workers

        Returns:
            Dictionary with valid, broken, and skipped links
        """
        self.link_config.max_workers = max_workers
        return self.link_checker.check_links_concurrent()

    def generate_component_inventory(self) -> dict[str, list[dict[str, Any]]]:
        """
        Generate component inventory from source code.

        Returns:
            Dictionary organized by component categories
        """
        return self.component_inventory.generate_inventory()

    def copy_file(
        self, src: str | Path, dst: str | Path, follow_symlinks: bool = True
    ) -> bool:
        """
        Copy a file using enhanced file operations.

        Args:
            src: Source path
            dst: Destination path
            follow_symlinks: Whether to follow symbolic links

        Returns:
            True if successful
        """
        return self.file_operations.copy_file(src, dst, follow_symlinks)

    def move_file(self, src: str | Path, dst: str | Path) -> bool:
        """
        Move a file using enhanced file operations.

        Args:
            src: Source path
            dst: Destination path

        Returns:
            True if successful
        """
        return self.file_operations.move_file(src, dst)
