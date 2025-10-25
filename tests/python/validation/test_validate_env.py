"""Tests for validate_env module."""

import os
from typing import Generator
from unittest.mock import patch

import pytest

from python.validation.validate_env import (
    main,
    print_summary,
    validate_env_vars,
)


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Clean environment variables for each test."""
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


class TestValidateEnvVars:
    """Test validate_env_vars function."""

    def test_all_required_vars_set(self, clean_env: None, capsys: pytest.CaptureFixture[str]) -> None:
        """Test validation passes when all required vars are set."""
        required_vars = [
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
        ]

        for var in required_vars:
            os.environ[var] = f"test_value_{var}"

        all_valid, missing_required, missing_optional = validate_env_vars()

        assert all_valid is True
        assert len(missing_required) == 0
        assert len(missing_optional) == 2  # DOCKER_ACCESS_TOKEN, CODECOV_TOKEN

        captured = capsys.readouterr()
        assert "Environment Variables Validation" in captured.out

    def test_missing_required_vars(self, clean_env: None, capsys: pytest.CaptureFixture[str]) -> None:
        """Test validation fails when required vars are missing."""
        # Set only some required vars
        os.environ["GITHUB_OWNER"] = "test_owner"
        os.environ["GH_PAT"] = "test_token"

        all_valid, missing_required, missing_optional = validate_env_vars()

        assert all_valid is False
        assert len(missing_required) > 0
        assert "DOCKER_POSTGRES_PASSWORD" in missing_required

        captured = capsys.readouterr()
        assert "NOT SET" in captured.out

    def test_optional_vars_set(self, clean_env: None, capsys: pytest.CaptureFixture[str]) -> None:
        """Test optional vars are recognized when set."""
        # Set all required vars
        required_vars = [
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
        ]

        for var in required_vars:
            os.environ[var] = f"test_{var}"

        # Set optional vars
        os.environ["DOCKER_ACCESS_TOKEN"] = "test_docker_token"
        os.environ["CODECOV_TOKEN"] = "test_codecov_token"

        all_valid, missing_required, missing_optional = validate_env_vars()

        assert all_valid is True
        assert len(missing_required) == 0
        assert len(missing_optional) == 0

    def test_no_vars_set(self, clean_env: None, capsys: pytest.CaptureFixture[str]) -> None:
        """Test validation with no environment variables set."""
        all_valid, missing_required, missing_optional = validate_env_vars()

        assert all_valid is False
        assert len(missing_required) == 11  # All 11 required vars
        assert len(missing_optional) == 2  # Both optional vars

    def test_value_masking(self, clean_env: None, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that sensitive values are masked in output."""
        os.environ["GH_PAT"] = "very_long_secret_token_value_12345"

        for var in [
            "GITHUB_OWNER",
            "DOCKER_POSTGRES_PASSWORD",
            "DOCKER_MARIADB_ROOT_PASSWORD",
            "DOCKER_MARIADB_PASSWORD",
            "DOCKER_REDIS_PASSWORD",
            "DOCKER_MINIO_ROOT_USER",
            "DOCKER_MINIO_ROOT_PASSWORD",
            "DOCKER_GRAFANA_ADMIN_PASSWORD",
            "DOCKER_JUPYTER_TOKEN",
            "DOCKER_PGADMIN_PASSWORD",
        ]:
            os.environ[var] = "test"

        validate_env_vars()

        captured = capsys.readouterr()
        assert "very_lon..." in captured.out
        assert "very_long_secret_token_value_12345" not in captured.out


class TestPrintSummary:
    """Test print_summary function."""

    def test_summary_all_valid(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test summary when all required vars are valid."""
        print_summary(True, [], [])

        captured = capsys.readouterr()
        assert "All required environment variables are set!" in captured.out
        assert "docker-compose up -d" in captured.out

    def test_summary_all_valid_with_optional_missing(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test summary when required vars are valid but optional missing."""
        print_summary(True, [], ["DOCKER_ACCESS_TOKEN"])

        captured = capsys.readouterr()
        assert "All required environment variables are set!" in captured.out
        assert "Optional variables missing:" in captured.out
        assert "DOCKER_ACCESS_TOKEN" in captured.out

    def test_summary_missing_required(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test summary when required vars are missing."""
        missing = ["GH_PAT", "DOCKER_POSTGRES_PASSWORD"]
        print_summary(False, missing, [])

        captured = capsys.readouterr()
        assert "Missing required environment variables!" in captured.out
        assert "GH_PAT" in captured.out
        assert "DOCKER_POSTGRES_PASSWORD" in captured.out
        assert ".env.example" in captured.out

    def test_summary_includes_fix_instructions(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test summary includes instructions for fixing issues."""
        print_summary(False, ["GH_PAT"], [])

        captured = capsys.readouterr()
        assert "To fix this:" in captured.out
        assert "cp .env.example .env" in captured.out
        assert "export" in captured.out or "Get-Content" in captured.out


class TestMain:
    """Test main function."""

    def test_main_success(self, clean_env: None) -> None:
        """Test main returns 0 on success."""
        # Set all required vars
        required_vars = [
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
        ]

        for var in required_vars:
            os.environ[var] = "test_value"

        exit_code = main()
        assert exit_code == 0

    def test_main_failure(self, clean_env: None) -> None:
        """Test main returns 1 on failure."""
        # Don't set any vars
        exit_code = main()
        assert exit_code == 1

    def test_main_partial_vars(self, clean_env: None) -> None:
        """Test main with partial vars set."""
        os.environ["GITHUB_OWNER"] = "test_owner"

        exit_code = main()
        assert exit_code == 1


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_string_values(self, clean_env: None) -> None:
        """Test that empty string values are treated as missing."""
        os.environ["GH_PAT"] = ""

        all_valid, missing_required, _ = validate_env_vars()

        assert all_valid is False
        # Empty string should be falsy, so GH_PAT should be in missing

    def test_short_value_masking(self, clean_env: None, capsys: pytest.CaptureFixture[str]) -> None:
        """Test masking of short values."""
        os.environ["GH_PAT"] = "short"

        for var in [
            "GITHUB_OWNER",
            "DOCKER_POSTGRES_PASSWORD",
            "DOCKER_MARIADB_ROOT_PASSWORD",
            "DOCKER_MARIADB_PASSWORD",
            "DOCKER_REDIS_PASSWORD",
            "DOCKER_MINIO_ROOT_USER",
            "DOCKER_MINIO_ROOT_PASSWORD",
            "DOCKER_GRAFANA_ADMIN_PASSWORD",
            "DOCKER_JUPYTER_TOKEN",
            "DOCKER_PGADMIN_PASSWORD",
        ]:
            os.environ[var] = "test"

        validate_env_vars()

        captured = capsys.readouterr()
        assert "***" in captured.out
        assert "short" not in captured.out

    def test_whitespace_values(self, clean_env: None) -> None:
        """Test that whitespace-only values are valid."""
        # Set all required vars with whitespace
        required_vars = [
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
        ]

        for var in required_vars:
            os.environ[var] = "   "  # Whitespace

        all_valid, missing_required, _ = validate_env_vars()

        # Whitespace values are truthy in Python
        assert all_valid is True
        assert len(missing_required) == 0
