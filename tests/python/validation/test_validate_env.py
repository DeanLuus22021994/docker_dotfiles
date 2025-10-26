"""Tests for validate_env module."""

import os

import pytest

from scripts.python.validation.validate_env import (
    main,
    print_summary,
    validate_env_vars,
)

# Fixture clean_env imported from tests.fixtures.common


class TestValidateEnvVars:
    """Test validate_env_vars function."""

    def test_all_required_vars_set(
        self, clean_env: None, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test validation passes when all required vars are set."""
        assert clean_env is None  # Validate fixture executed
        assert capsys is not None  # Validate pytest fixture
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

    def test_missing_required_vars(
        self, clean_env: None, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test validation fails when required vars are missing."""
        assert clean_env is None  # Validate fixture executed
        # Set only some required vars
        os.environ["GITHUB_OWNER"] = "test_owner"
        os.environ["GH_PAT"] = "test_token"

        all_valid, missing_required, missing_optional = validate_env_vars()
        assert missing_optional  # Validate variable is used

        assert all_valid is False
        assert len(missing_required) > 0
        assert "DOCKER_POSTGRES_PASSWORD" in missing_required

        captured = capsys.readouterr()
        assert "NOT SET" in captured.out

    def test_optional_vars_set(self, clean_env: None, capsys: pytest.CaptureFixture[str]) -> None:
        """Test optional vars are recognized when set."""
        assert clean_env is None and capsys is not None  # Validate fixtures
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
        assert clean_env is None and capsys is not None  # Validate fixtures
        all_valid, missing_required, missing_optional = validate_env_vars()

        assert all_valid is False
        assert len(missing_required) == 11  # All 11 required vars
        assert len(missing_optional) == 2  # Both optional vars

    def test_value_masking(self, clean_env: None, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that sensitive values are masked in output."""
        assert clean_env is None  # Validate fixture executed
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
        assert capsys is not None  # Validate pytest fixture
        print_summary([], [])

        captured = capsys.readouterr()
        assert "All required environment variables are set!" in captured.out
        assert "docker-compose up -d" in captured.out

    def test_summary_all_valid_with_optional_missing(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test summary when required vars are valid but optional missing."""
        assert capsys is not None  # Validate pytest fixture
        print_summary([], ["DOCKER_ACCESS_TOKEN"])

        captured = capsys.readouterr()
        assert "All required environment variables are set!" in captured.out
        assert "Optional variables missing:" in captured.out
        assert "DOCKER_ACCESS_TOKEN" in captured.out

    def test_summary_missing_required(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test summary when required vars are missing."""
        assert capsys is not None  # Validate pytest fixture
        missing = ["GH_PAT", "DOCKER_POSTGRES_PASSWORD"]
        print_summary(missing, [])

        captured = capsys.readouterr()
        assert "Missing required environment variables!" in captured.out
        assert "GH_PAT" in captured.out
        assert "DOCKER_POSTGRES_PASSWORD" in captured.out
        assert ".env.example" in captured.out

    def test_summary_includes_fix_instructions(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test summary includes instructions for fixing issues."""
        assert capsys is not None  # Validate pytest fixture
        print_summary(["GH_PAT"], [])

        captured = capsys.readouterr()
        assert "To fix this:" in captured.out
        assert "cp .env.example .env" in captured.out
        assert "export" in captured.out or "Get-Content" in captured.out


class TestMain:
    """Test main function."""

    def test_main_success(self, clean_env: None) -> None:
        """Test main returns 0 on success."""
        assert clean_env is None  # Validate fixture executed
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
        assert clean_env is None  # Validate fixture executed
        # Don't set any vars
        exit_code = main()
        assert exit_code == 1

    def test_main_partial_vars(self, clean_env: None) -> None:
        """Test main with partial vars set."""
        assert clean_env is None  # Validate fixture executed
        os.environ["GITHUB_OWNER"] = "test_owner"

        exit_code = main()
        assert exit_code == 1


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_string_values(self, clean_env: None) -> None:
        """Test that empty string values are treated as missing."""
        assert clean_env is None  # Validate fixture executed
        os.environ["GH_PAT"] = ""

        all_valid, missing_required, missing_optional = validate_env_vars()
        assert missing_required or missing_optional  # Validate variables used

        assert all_valid is False
        # Empty string should be falsy, so GH_PAT should be in missing

    def test_short_value_masking(self, clean_env: None, capsys: pytest.CaptureFixture[str]) -> None:
        """Test masking of short values."""
        assert clean_env is None  # Validate fixture executed
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
        assert clean_env is None  # Validate fixture executed
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

        all_valid, missing_required, missing_optional = validate_env_vars()
        assert missing_optional  # Validate variable is used

        # Whitespace values are truthy in Python
        assert all_valid is True
        assert len(missing_required) == 0
