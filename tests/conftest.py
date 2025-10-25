"""Pytest configuration and shared fixtures."""

import sys
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "scripts"))


@pytest.fixture
def project_root_path() -> Path:
    """Return the project root directory path."""
    return Path(__file__).parent.parent


@pytest.fixture
def scripts_path(project_root_path: Path) -> Path:
    """Return the scripts directory path."""
    return project_root_path / "scripts"


@pytest.fixture
def fixtures_path() -> Path:
    """Return the test fixtures directory path."""
    return Path(__file__).parent / "fixtures"
