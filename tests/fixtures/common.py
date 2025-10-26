"""Common test fixtures for all test modules.

This module provides standardized fixtures for:
- Temporary directories and files
- Environment variable management
- Logger cleanup
- JSON and text file creation
- Project directory structures

These fixtures ensure separation of concerns and eliminate duplication across tests.
"""

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest


# ============================================================================
# Temporary Directory and File Fixtures
# ============================================================================


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing.

    Yields:
        Path to temporary directory that is automatically cleaned up after test.

    Example:
        def test_something(temp_dir: Path) -> None:
            test_file = temp_dir / "test.txt"
            test_file.write_text("content")
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_project_dir(temp_dir: Path) -> Path:
    """Create temporary project directory structure.

    Creates standard project structure:
    - .config/nginx/
    - .config/database/

    Args:
        temp_dir: Base temporary directory from temp_dir fixture

    Returns:
        Path to project root directory

    Example:
        def test_config(temp_project_dir: Path) -> None:
            nginx_conf = temp_project_dir / ".config" / "nginx" / "main.conf"
    """
    base_dir = temp_dir
    (base_dir / ".config" / "nginx").mkdir(parents=True)
    (base_dir / ".config" / "database").mkdir(parents=True)
    return base_dir


@pytest.fixture
def sample_json_file(temp_dir: Path) -> Path:
    """Create sample JSON file for testing.

    Creates file with structure:
    {
        "name": "test",
        "value": 42,
        "items": ["a", "b", "c"]
    }

    Args:
        temp_dir: Temporary directory for file from temp_dir fixture

    Returns:
        Path to created JSON file

    Example:
        def test_read_json(sample_json_file: Path) -> None:
            data = json.loads(sample_json_file.read_text())
            assert data["name"] == "test"
    """
    base_dir = temp_dir
    file_path = base_dir / "sample.json"
    data = {"name": "test", "value": 42, "items": ["a", "b", "c"]}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return file_path


@pytest.fixture
def sample_text_file(temp_dir: Path) -> Path:
    """Create sample text file for testing.

    Creates file with three lines: "line1", "line2", "line3"

    Args:
        temp_dir: Temporary directory for file from temp_dir fixture

    Returns:
        Path to created text file

    Example:
        def test_read_lines(sample_text_file: Path) -> None:
            lines = sample_text_file.read_text().splitlines()
            assert len(lines) == 3
    """
    base_dir = temp_dir
    file_path = base_dir / "sample.txt"
    content = "line1\nline2\nline3\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


# ============================================================================
# Environment Variable Fixtures
# ============================================================================


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Clean environment variables for each test.

    Stores and restores all Docker and GitHub environment variables:
    - GITHUB_OWNER
    - GH_PAT
    - DOCKER_POSTGRES_PASSWORD
    - DOCKER_MARIADB_ROOT_PASSWORD
    - DOCKER_MARIADB_PASSWORD
    - DOCKER_REDIS_PASSWORD
    - DOCKER_MINIO_ROOT_USER
    - DOCKER_MINIO_ROOT_PASSWORD
    - DOCKER_GRAFANA_ADMIN_PASSWORD
    - DOCKER_JUPYTER_TOKEN
    - DOCKER_PGADMIN_PASSWORD
    - DOCKER_ACCESS_TOKEN
    - CODECOV_TOKEN

    Yields:
        None (environment is cleaned before test, restored after)

    Example:
        def test_env_vars(clean_env: None) -> None:
            # All env vars cleared
            os.environ["GH_PAT"] = "test_token"
            # After test, original value restored
    """
    env_vars = [
        "GITHUB_OWNER",
        "GH_PAT",
        "DOCKER_POSTGRES_PASSWORD",
        "DOCKER_MARIADB_ROOT_PASSWORD",
        "DOCKER_MARIADB_PASSWORD",
        "DOCKER_REDIS_PASSWORD",
        "DOCKER_MINIO_ROOT_USER",
        "DOCKER_MINIO_ROOT_PASSWORD",
        "DOCKER_GRAFANA_ADMIN_PASSWORD",
        "DOCKER_JUPYTER_TOKEN",
        "DOCKER_PGADMIN_PASSWORD",
        "DOCKER_ACCESS_TOKEN",
        "CODECOV_TOKEN",
    ]

    # Store original values
    original_values = {var: os.environ.get(var) for var in env_vars}

    # Clear all test environment variables
    for var in env_vars:
        os.environ.pop(var, None)

    yield

    # Restore original values
    for var, value in original_values.items():
        if value is not None:
            os.environ[var] = value
        else:
            os.environ.pop(var, None)


# ============================================================================
# Logger Cleanup Fixtures
# ============================================================================


@pytest.fixture
def cleanup_loggers() -> Generator[None, None, None]:
    """Cleanup loggers after each test.

    Clears all handlers and resets log levels for all loggers to prevent
    interference between tests.

    Yields:
        None (cleanup happens after test execution)

    Example:
        def test_logger(cleanup_loggers: None) -> None:
            logger = logging.getLogger("test")
            # Logger automatically cleaned up after test
    """
    yield
    # Clear all logger handlers
    for logger_name in list(logging.Logger.manager.loggerDict.keys()):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.setLevel(logging.NOTSET)
