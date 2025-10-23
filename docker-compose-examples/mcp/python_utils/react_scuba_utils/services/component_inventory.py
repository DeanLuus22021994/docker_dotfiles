"""
Component inventory service for React Scuba.

This module provides functionality to analyze and catalog React components,
hooks, utilities, and pages in the source codebase.
"""

import re
import sys
from pathlib import Path
from typing import Any

from ..config.settings import PathConfig
from ..models.models import ComponentInfo, ComponentInventoryConfig


class ComponentInventoryService:
    """
    Service for generating component inventories.

    Analyzes React/TypeScript source files to extract component information,
    dependencies, and metadata.
    """

    def __init__(
        self, config: ComponentInventoryConfig, path_config: PathConfig
    ) -> None:
        self.config = config
        self.path_config = path_config

    def generate_inventory(self) -> dict[str, list[dict[str, Any]]]:
        """
        Generate a comprehensive inventory of components.

        Returns a dictionary organized by component categories.
        """
        components: dict[str, list[dict[str, Any]]] = {
            category: [] for category in self.config.categories
        }

        src_path = self.path_config.resolve_src_path()
        component_files = self._find_component_files(src_path)

        for file_path in component_files:
            try:
                component_info = self._analyze_component_file(file_path)
                if component_info:
                    category = component_info.category
                    if category in components:
                        components[category].append(component_info.to_dict())

            except Exception as e:
                print(f"Error processing {file_path}: {e}", file=sys.stderr)

        return components

    def _find_component_files(self, src_path: Path) -> list[Path]:
        extensions = ["*.jsx", "*.js", "*.tsx", "*.ts"]
        component_files: list[Path] = []
        for ext in extensions:
            component_files.extend(src_path.rglob(ext))
        return component_files

    def _analyze_component_file(self, file_path: Path) -> ComponentInfo | None:
        try:
            content = file_path.read_text(encoding="utf-8")
            size_bytes = file_path.stat().st_size

            relative_path = file_path.relative_to(self.path_config.src_path)
            category = self._determine_category(str(relative_path))

            component_info = self._extract_component_info(content, file_path, category)
            if component_info:
                component_info.size_bytes = size_bytes

            return component_info

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}", file=sys.stderr)
            return None

    def _determine_category(self, relative_path: str) -> str:
        """Determine component category based on file path."""
        path_lower = relative_path.lower()

        if "page" in path_lower or "screen" in path_lower:
            return "pages"
        elif "hook" in path_lower:
            return "hooks"
        elif "util" in path_lower or "helper" in path_lower:
            return "utils"
        else:
            return "components"

    def _extract_component_info(
        self, content: str, file_path: Path, category: str
    ) -> ComponentInfo | None:
        component_name = self._extract_component_name(content, file_path.name)
        if not component_name:
            return None

        exports = self._extract_exports(content)
        imports = self._extract_imports(content)

        return ComponentInfo(
            name=component_name,
            file=str(file_path.relative_to(file_path.parents[2])),
            path=str(file_path),
            category=category,
            exports=exports,
            imports=imports,
            size_bytes=0,
        )

    def _extract_component_name(self, content: str, filename: str) -> str | None:
        patterns = [
            r"export default (\w+)",
            r"export \{ default as (\w+) \}",
            r"(?:export )?(?:const|function|class) (\w+)",
            r"module\.exports = (\w+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)

        return (
            filename.replace(".jsx", "")
            .replace(".js", "")
            .replace(".tsx", "")
            .replace(".ts", "")
        )

    def _extract_exports(self, content: str) -> list[str]:
        exports = []

        named_exports = re.findall(
            r"export (?:const|function|class|let|var) (\w+)", content
        )
        exports.extend(named_exports)

        export_statements = re.findall(r"export \{([^}]+)\}", content)
        for statement in export_statements:
            items = [item.split(" as ")[0].strip() for item in statement.split(",")]
            exports.extend(items)

        return list(set(exports))

    def _extract_imports(self, content: str) -> list[str]:
        imports = []

        es6_imports = re.findall(r'import .* from ["\']([^"\']+)["\']', content)
        imports.extend(es6_imports)

        cjs_imports = re.findall(r'require\(["\']([^"\']+)["\']', content)
        imports.extend(cjs_imports)

        return list(set(imports))
