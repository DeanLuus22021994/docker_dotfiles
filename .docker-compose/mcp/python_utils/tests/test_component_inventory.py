"""
Unit tests for ComponentInventoryService.

Comprehensive test coverage for component analysis functionality,
including file parsing, inventory generation, and data extraction.
"""

from pathlib import Path
from unittest.mock import patch

import pytest

from docker_examples_utils.config.settings import PathConfig
from docker_examples_utils.models.models import ComponentInventoryConfig
from docker_examples_utils.services.component_inventory import ComponentInventoryService


class TestComponentInventoryService:
    """Test suite for ComponentInventoryService."""

    @pytest.fixture
    def config(self) -> ComponentInventoryConfig:
        """Create test configuration."""
        return ComponentInventoryConfig(
            src_path="src",
            extensions=["*.jsx", "*.js", "*.tsx", "*.ts"],
            categories=["pages", "components", "hooks", "utils"]
        )

    @pytest.fixture
    def path_config(self, tmp_path: Path) -> PathConfig:
        """Create test path configuration."""
        return PathConfig(
            docs_path=tmp_path / "docs",
            src_path=tmp_path / "src",
            base_url="https://example.com"
        )

    @pytest.fixture
    def service(self, config: ComponentInventoryConfig, path_config: PathConfig) -> ComponentInventoryService:
        """Create ComponentInventoryService instance."""
        return ComponentInventoryService(config, path_config)

    @pytest.fixture
    def sample_files(self, tmp_path: Path) -> dict[str, Path]:
        """Create sample component files for testing."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()

        # Create sample React component
        component_file = src_dir / "Button.jsx"
        component_file.write_text("""
import React from 'react';

export default function Button({ children, onClick }) {
  return (
    <button className="btn" onClick={onClick}>
      {children}
    </button>
  );
}

export const ButtonVariant = {
  PRIMARY: 'primary',
  SECONDARY: 'secondary'
};
""")

        # Create sample page component
        page_file = src_dir / "pages" / "HomePage.tsx"
        page_file.parent.mkdir(exist_ok=True)
        page_file.write_text("""
import React from 'react';
import { Button } from '../Button';

export default function HomePage() {
  return (
    <div>
      <h1>Home Page</h1>
      <Button onClick={() => console.log('click')}>Click me</Button>
    </div>
  );
}
""")

        # Create sample hook
        hook_file = src_dir / "hooks" / "useCounter.ts"
        hook_file.parent.mkdir(exist_ok=True)
        hook_file.write_text("""
import { useState } from 'react';

export function useCounter(initialValue: number = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount(count + 1);
  const decrement = () => setCount(count - 1);

  return { count, increment, decrement };
}
""")

        # Create sample utility
        util_file = src_dir / "utils" / "helpers.js"
        util_file.parent.mkdir(exist_ok=True)
        util_file.write_text("""
export function formatDate(date) {
  return date.toLocaleDateString();
}

export const API_BASE_URL = 'https://api.example.com';
""")

        return {
            "component": component_file,
            "page": page_file,
            "hook": hook_file,
            "util": util_file,
        }

    def test_init(self, service: ComponentInventoryService, config: ComponentInventoryConfig, path_config: PathConfig):
        """Test service initialization."""
        assert service.config == config
        assert service.path_config == path_config

    def test_generate_inventory_comprehensive(
        self, service: ComponentInventoryService, sample_files: dict[str, Path]
    ):
        """Test comprehensive inventory generation."""
        inventory = service.generate_inventory()

        # Check that all categories exist
        assert "pages" in inventory
        assert "components" in inventory
        assert "hooks" in inventory
        assert "utils" in inventory

        # Check specific components
        components = inventory["components"]
        assert len(components) >= 1

        # Find Button component
        button_component = next((c for c in components if c["name"] == "Button"), None)
        assert button_component is not None
        assert "ButtonVariant" in button_component["exports"]
        assert button_component["category"] == "components"
        assert button_component["size_bytes"] > 0

        # Check pages
        pages = inventory["pages"]
        assert len(pages) >= 1
        home_page = next((p for p in pages if p["name"] == "HomePage"), None)
        assert home_page is not None
        assert home_page["category"] == "pages"

        # Check hooks
        hooks = inventory["hooks"]
        assert len(hooks) >= 1
        counter_hook = next((h for h in hooks if h["name"] == "useCounter"), None)
        assert counter_hook is not None
        assert counter_hook["category"] == "hooks"
        assert "useCounter" in counter_hook["exports"]

        # Check utils
        utils = inventory["utils"]
        assert len(utils) >= 1
        helpers_util = next((u for u in utils if u["name"] == "helpers"), None)
        assert helpers_util is not None
        assert helpers_util["category"] == "utils"
        assert "formatDate" in helpers_util["exports"]
        assert "API_BASE_URL" in helpers_util["exports"]

    def test_generate_inventory_empty_directory(
        self, service: ComponentInventoryService, tmp_path: Path
    ):
        """Test inventory generation with empty directory."""
        empty_dir = tmp_path / "empty_src"
        empty_dir.mkdir()

        # Temporarily change src_path
        original_src = service.path_config.src_path
        service.path_config.src_path = empty_dir

        try:
            inventory = service.generate_inventory()

            # Should have empty categories
            for category in service.config.categories:
                assert category in inventory
                assert inventory[category] == []
        finally:
            service.path_config.src_path = original_src

    def test_generate_inventory_file_processing_error(
        self, service: ComponentInventoryService, sample_files: dict[str, Path]
    ):
        """Test inventory generation handles file processing errors gracefully."""
        # Mock the internal _analyze_component_file method to raise an exception
        with patch.object(service, '_analyze_component_file', side_effect=Exception("Processing error")):
            inventory = service.generate_inventory()

        # Should still generate inventory structure even with errors
        assert isinstance(inventory, dict)
        assert all(isinstance(v, list) for v in inventory.values())

    def test_inventory_categories_from_config(self, service: ComponentInventoryService):
        """Test that inventory uses categories from configuration."""
        inventory = service.generate_inventory()

        # Should have exactly the categories from config
        assert set(inventory.keys()) == set(service.config.categories)

    def test_component_analysis_includes_imports(
        self, service: ComponentInventoryService, sample_files: dict[str, Path]
    ):
        """Test that component analysis includes import information."""
        inventory = service.generate_inventory()

        # Check Button component imports
        components = inventory["components"]
        button_component = next((c for c in components if c["name"] == "Button"), None)
        assert button_component is not None
        assert "react" in button_component["imports"]

        # Check HomePage component imports
        pages = inventory["pages"]
        home_page = next((p for p in pages if p["name"] == "HomePage"), None)
        assert home_page is not None
        assert "../Button" in home_page["imports"]
        assert "react" in home_page["imports"]

    def test_component_analysis_includes_file_info(
        self, service: ComponentInventoryService, sample_files: dict[str, Path]
    ):
        """Test that component analysis includes file path and size information."""
        inventory = service.generate_inventory()

        # Check that all components have file_path and size_bytes
        for _, components in inventory.items():
            for component in components:
                assert "file_path" in component
                assert "size_bytes" in component
                assert isinstance(component["size_bytes"], int)
                assert component["size_bytes"] > 0
                assert "relative_path" in component

    def test_component_analysis_handles_different_export_patterns(
        self, service: ComponentInventoryService, tmp_path: Path
    ):
        """Test component analysis with different export patterns."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()

        # Create component with named exports
        named_export_file = src_dir / "NamedExports.js"
        named_export_file.write_text("""
export function ComponentA() { return 'A'; }
export function ComponentB() { return 'B'; }
export const CONSTANT = 'value';
""")

        # Create component with default export
        default_export_file = src_dir / "DefaultExport.ts"
        default_export_file.write_text("""
export default class MyClass {
  method() { return 'test'; }
}
""")

        # Create component with mixed exports
        mixed_export_file = src_dir / "MixedExports.tsx"
        mixed_export_file.write_text("""
import React from 'react';

export default function MainComponent() {
  return <div>Main</div>;
}

export const Helper = () => <div>Helper</div>;
export { OtherComponent } from './Other';
""")

        inventory = service.generate_inventory()

        components = inventory["components"]

        # Find and verify named exports component
        named_comp = next((c for c in components if c["name"] == "NamedExports"), None)
        assert named_comp is not None
        assert "ComponentA" in named_comp["exports"]
        assert "ComponentB" in named_comp["exports"]
        assert "CONSTANT" in named_comp["exports"]

        # Find and verify default export component
        default_comp = next((c for c in components if c["name"] == "DefaultExport"), None)
        assert default_comp is not None
        assert "MyClass" in default_comp["exports"]

        # Find and verify mixed exports component
        mixed_comp = next((c for c in components if c["name"] == "MixedExports"), None)
        assert mixed_comp is not None
        assert "MainComponent" in mixed_comp["exports"]
        assert "Helper" in mixed_comp["exports"]
        assert "react" in mixed_comp["imports"]

    def test_component_analysis_error_handling(
        self, service: ComponentInventoryService, tmp_path: Path
    ):
        """Test error handling during component analysis."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()

        # Create a file that will cause read error
        error_file = src_dir / "error.jsx"
        error_file.write_text("valid content")

        # Mock read_text to raise UnicodeDecodeError
        def mock_read(self: Path) -> str:
            if self.name == "error.jsx":
                raise UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid')
            return self.read_text()

        with patch.object(Path, 'read_text', mock_read):
            inventory = service.generate_inventory()

        # Should still generate inventory, but error file should be skipped
        assert isinstance(inventory, dict)
        # Error file should not appear in any category
        all_components = []
        for category_components in inventory.values():
            all_components.extend(category_components)  # type: ignore

        error_components = [c for c in all_components if "error.jsx" in str(c.get("file_path", ""))]  # type: ignore
        assert len(error_components) == 0  # type: ignore
