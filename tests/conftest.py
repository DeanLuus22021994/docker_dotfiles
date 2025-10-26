"""Pytest configuration and shared fixtures."""

import sys
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "scripts"))

# Import common fixtures to make them globally available
pytest_plugins = ["tests.fixtures.common"]


@pytest.fixture
def scripts_path() -> Path:
    """Return the scripts directory path."""
    return project_root / "scripts"


@pytest.fixture
def fixtures_path() -> Path:
    """Return the test fixtures directory path."""
    return Path(__file__).parent / "fixtures"
