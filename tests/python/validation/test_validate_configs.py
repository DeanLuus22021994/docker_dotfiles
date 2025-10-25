"""Tests for validate_configs module."""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, Mock, patch

import pytest

from python.validation.validate_configs import (
    main,
    validate_json_files,
    validate_mariadb_config,
    validate_nginx_configs,
    validate_postgresql_config,
    validate_yaml_files,
)


@pytest.fixture
def temp_project_dir() -> Generator[Path, None, None]:
    """Create temporary project directory structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)

        # Create directory structure
        (project_dir / ".config" / "nginx").mkdir(parents=True)
        (project_dir / ".config" / "database").mkdir(parents=True)

        yield project_dir


class TestValidateYamlFiles:
    """Test validate_yaml_files function."""

    @patch("subprocess.run")
    @patch("pathlib.Path.rglob")
    def test_validate_yaml_success(
        self, mock_rglob: Mock, mock_run: Mock
    ) -> None:
        """Test successful YAML validation."""
        mock_rglob.return_value = [Path("test.yml"), Path("config.yaml")]
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        passed, errors = validate_yaml_files()

        assert passed is True
        assert len(errors) == 0
        mock_run.assert_called_once()

    @patch("subprocess.run")
    @patch("pathlib.Path.rglob")
    def test_validate_yaml_failure(
        self, mock_rglob: Mock, mock_run: Mock
    ) -> None:
        """Test YAML validation failure."""
        mock_rglob.return_value = [Path("test.yml")]
        mock_run.return_value = Mock(
            returncode=1, stdout="test.yml: line 10: syntax error", stderr=""
        )

        passed, errors = validate_yaml_files()

        assert passed is False
        assert len(errors) == 1
        assert "yamllint failed" in errors[0]

    @patch("subprocess.run", side_effect=FileNotFoundError())
    @patch("pathlib.Path.rglob")
    def test_validate_yaml_no_yamllint(
        self, mock_rglob: Mock, mock_run: Mock
    ) -> None:
        """Test YAML validation when yamllint is not installed."""
        mock_rglob.return_value = [Path("test.yml")]

        passed, errors = validate_yaml_files()

        assert passed is False
        assert len(errors) == 1
        assert "yamllint not found" in errors[0]

    @patch("pathlib.Path.rglob")
    def test_validate_yaml_no_files(self, mock_rglob: Mock) -> None:
        """Test YAML validation with no files."""
        mock_rglob.return_value = []

        passed, errors = validate_yaml_files()

        assert passed is True
        assert len(errors) == 0


class TestValidateJsonFiles:
    """Test validate_json_files function."""

    def test_validate_json_success(self, temp_project_dir: Path) -> None:
        """Test successful JSON validation."""
        json_file = temp_project_dir / "test.json"
        json_file.write_text(json.dumps({"key": "value"}), encoding="utf-8")

        with patch("pathlib.Path.rglob", return_value=[json_file]):
            passed, errors = validate_json_files()

        assert passed is True
        assert len(errors) == 0

    def test_validate_json_invalid(self, temp_project_dir: Path) -> None:
        """Test JSON validation with invalid file."""
        json_file = temp_project_dir / "invalid.json"
        json_file.write_text("{invalid json", encoding="utf-8")

        with patch("pathlib.Path.rglob", return_value=[json_file]):
            passed, errors = validate_json_files()

        assert passed is False
        assert len(errors) == 1
        assert "invalid.json" in errors[0]

    def test_validate_json_no_files(self) -> None:
        """Test JSON validation with no files."""
        with patch("pathlib.Path.rglob", return_value=[]):
            passed, errors = validate_json_files()

        assert passed is True
        assert len(errors) == 0

    def test_validate_json_excludes_vscode(self, temp_project_dir: Path) -> None:
        """Test JSON validation excludes .vscode directory."""
        vscode_json = temp_project_dir / ".vscode" / "settings.json"
        vscode_json.parent.mkdir()
        vscode_json.write_text('{"key": "value"}', encoding="utf-8")

        with patch("pathlib.Path.rglob", return_value=[vscode_json]):
            passed, errors = validate_json_files()

        # Should skip .vscode files
        assert passed is True
        assert len(errors) == 0

    def test_validate_json_multiple_files(self, temp_project_dir: Path) -> None:
        """Test JSON validation with multiple files."""
        json1 = temp_project_dir / "file1.json"
        json2 = temp_project_dir / "file2.json"
        json3 = temp_project_dir / "invalid.json"

        json1.write_text('{"valid": true}', encoding="utf-8")
        json2.write_text('{"also": "valid"}', encoding="utf-8")
        json3.write_text('{invalid}', encoding="utf-8")

        with patch("pathlib.Path.rglob", return_value=[json1, json2, json3]):
            passed, errors = validate_json_files()

        assert passed is False
        assert len(errors) == 1


class TestValidateNginxConfigs:
    """Test validate_nginx_configs function."""

    @patch("subprocess.run")
    def test_validate_nginx_success(
        self, mock_run: Mock, temp_project_dir: Path
    ) -> None:
        """Test successful nginx validation."""
        nginx_config = temp_project_dir / ".config" / "nginx" / "main.conf"
        nginx_config.parent.mkdir(parents=True, exist_ok=True)
        nginx_config.write_text("# nginx config", encoding="utf-8")

        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        with patch("pathlib.Path.exists", return_value=True):
            passed, errors = validate_nginx_configs()

        assert passed is True
        assert len(errors) == 0

    @patch("subprocess.run")
    def test_validate_nginx_failure(
        self, mock_run: Mock, temp_project_dir: Path
    ) -> None:
        """Test nginx validation failure."""
        mock_run.return_value = Mock(
            returncode=1, stdout="", stderr="nginx: configuration error"
        )

        with patch("pathlib.Path.exists", return_value=True):
            passed, errors = validate_nginx_configs()

        assert passed is False
        assert len(errors) > 0

    @patch("subprocess.run", side_effect=FileNotFoundError())
    def test_validate_nginx_no_docker(self, mock_run: Mock) -> None:
        """Test nginx validation when Docker is not available."""
        with patch("pathlib.Path.exists", return_value=True):
            passed, errors = validate_nginx_configs()

        assert passed is False
        assert "Docker not found" in errors[0]

    def test_validate_nginx_no_configs(self) -> None:
        """Test nginx validation with no config files."""
        with patch("pathlib.Path.exists", return_value=False):
            passed, errors = validate_nginx_configs()

        assert passed is True
        assert len(errors) == 0


class TestValidatePostgresqlConfig:
    """Test validate_postgresql_config function."""

    def test_validate_postgresql_success(self, temp_project_dir: Path) -> None:
        """Test successful PostgreSQL config validation."""
        pg_config = temp_project_dir / ".config" / "database" / "postgresql.conf"
        pg_config.parent.mkdir(parents=True, exist_ok=True)
        pg_config.write_text(
            "# PostgreSQL configuration\nmax_connections = 100\n", encoding="utf-8"
        )

        with patch(
            "pathlib.Path.exists", return_value=True
        ), patch(
            "builtins.open",
            return_value=open(pg_config, "r", encoding="utf-8"),
        ):
            passed, errors = validate_postgresql_config()

        assert passed is True
        assert len(errors) == 0

    def test_validate_postgresql_invalid_syntax(
        self, temp_project_dir: Path
    ) -> None:
        """Test PostgreSQL config with invalid syntax."""
        pg_config = temp_project_dir / ".config" / "database" / "postgresql.conf"
        pg_config.parent.mkdir(parents=True, exist_ok=True)
        pg_config.write_text("invalid_line_without_equals\n", encoding="utf-8")

        with patch(
            "pathlib.Path.exists", return_value=True
        ), patch(
            "builtins.open",
            return_value=open(pg_config, "r", encoding="utf-8"),
        ):
            passed, errors = validate_postgresql_config()

        assert passed is False
        assert len(errors) == 1

    def test_validate_postgresql_comments_ignored(
        self, temp_project_dir: Path
    ) -> None:
        """Test PostgreSQL config ignores comments."""
        pg_config = temp_project_dir / ".config" / "database" / "postgresql.conf"
        pg_config.parent.mkdir(parents=True, exist_ok=True)
        pg_config.write_text(
            "# This is a comment\nmax_connections = 100\n", encoding="utf-8"
        )

        with patch(
            "pathlib.Path.exists", return_value=True
        ), patch(
            "builtins.open",
            return_value=open(pg_config, "r", encoding="utf-8"),
        ):
            passed, errors = validate_postgresql_config()

        assert passed is True
        assert len(errors) == 0

    def test_validate_postgresql_no_config(self) -> None:
        """Test PostgreSQL validation with no config file."""
        with patch("pathlib.Path.exists", return_value=False):
            passed, errors = validate_postgresql_config()

        assert passed is True
        assert len(errors) == 0


class TestValidateMariadbConfig:
    """Test validate_mariadb_config function."""

    def test_validate_mariadb_success(self, temp_project_dir: Path) -> None:
        """Test successful MariaDB config validation."""
        maria_config = temp_project_dir / ".config" / "database" / "mariadb.conf"
        maria_config.parent.mkdir(parents=True, exist_ok=True)
        maria_config.write_text(
            "[mysqld]\nmax_connections = 100\n", encoding="utf-8"
        )

        with patch(
            "pathlib.Path.exists", return_value=True
        ), patch(
            "builtins.open",
            return_value=open(maria_config, "r", encoding="utf-8"),
        ):
            passed, errors = validate_mariadb_config()

        assert passed is True
        assert len(errors) == 0

    def test_validate_mariadb_invalid_syntax(
        self, temp_project_dir: Path
    ) -> None:
        """Test MariaDB config with invalid syntax."""
        maria_config = temp_project_dir / ".config" / "database" / "mariadb.conf"
        maria_config.parent.mkdir(parents=True, exist_ok=True)
        maria_config.write_text("[mysqld]\ninvalid line\n", encoding="utf-8")

        with patch(
            "pathlib.Path.exists", return_value=True
        ), patch(
            "builtins.open",
            return_value=open(maria_config, "r", encoding="utf-8"),
        ):
            passed, errors = validate_mariadb_config()

        assert passed is False
        assert len(errors) == 1

    def test_validate_mariadb_no_config(self) -> None:
        """Test MariaDB validation with no config file."""
        with patch("pathlib.Path.exists", return_value=False):
            passed, errors = validate_mariadb_config()

        assert passed is True
        assert len(errors) == 0


class TestMain:
    """Test main function."""

    @patch("python.validation.validate_configs.validate_yaml_files")
    @patch("python.validation.validate_configs.validate_json_files")
    @patch("python.validation.validate_configs.validate_nginx_configs")
    @patch("python.validation.validate_configs.validate_postgresql_config")
    @patch("python.validation.validate_configs.validate_mariadb_config")
    def test_main_all_pass(
        self,
        mock_maria: Mock,
        mock_pg: Mock,
        mock_nginx: Mock,
        mock_json: Mock,
        mock_yaml: Mock,
    ) -> None:
        """Test main returns 0 when all validations pass."""
        mock_yaml.return_value = (True, [])
        mock_json.return_value = (True, [])
        mock_nginx.return_value = (True, [])
        mock_pg.return_value = (True, [])
        mock_maria.return_value = (True, [])

        exit_code = main()

        assert exit_code == 0

    @patch("python.validation.validate_configs.validate_yaml_files")
    @patch("python.validation.validate_configs.validate_json_files")
    @patch("python.validation.validate_configs.validate_nginx_configs")
    @patch("python.validation.validate_configs.validate_postgresql_config")
    @patch("python.validation.validate_configs.validate_mariadb_config")
    def test_main_some_fail(
        self,
        mock_maria: Mock,
        mock_pg: Mock,
        mock_nginx: Mock,
        mock_json: Mock,
        mock_yaml: Mock,
    ) -> None:
        """Test main returns 1 when some validations fail."""
        mock_yaml.return_value = (True, [])
        mock_json.return_value = (False, ["JSON error"])
        mock_nginx.return_value = (True, [])
        mock_pg.return_value = (False, ["PostgreSQL error"])
        mock_maria.return_value = (True, [])

        exit_code = main()

        assert exit_code == 1

    @patch("python.validation.validate_configs.validate_yaml_files")
    @patch("python.validation.validate_configs.validate_json_files")
    @patch("python.validation.validate_configs.validate_nginx_configs")
    @patch("python.validation.validate_configs.validate_postgresql_config")
    @patch("python.validation.validate_configs.validate_mariadb_config")
    def test_main_all_fail(
        self,
        mock_maria: Mock,
        mock_pg: Mock,
        mock_nginx: Mock,
        mock_json: Mock,
        mock_yaml: Mock,
    ) -> None:
        """Test main returns 1 when all validations fail."""
        mock_yaml.return_value = (False, ["YAML error"])
        mock_json.return_value = (False, ["JSON error"])
        mock_nginx.return_value = (False, ["nginx error"])
        mock_pg.return_value = (False, ["PostgreSQL error"])
        mock_maria.return_value = (False, ["MariaDB error"])

        exit_code = main()

        assert exit_code == 1
