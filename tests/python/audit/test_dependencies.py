"""Tests for dependencies module."""

import sys
from unittest.mock import Mock, patch

import pytest

from python.audit.dependencies import (
    check_outdated_packages,
    check_pyproject_dependencies,
    list_installed_packages,
    main,
)


class TestCheckOutdatedPackages:
    """Test check_outdated_packages function."""

    @patch("subprocess.run")
    def test_no_outdated_packages(self, mock_run: Mock) -> None:
        """Test when all packages are up to date."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        passed, errors = check_outdated_packages()

        assert passed is True
        assert len(errors) == 0

    @patch("subprocess.run")
    def test_outdated_packages_found(self, mock_run: Mock) -> None:
        """Test when outdated packages are found."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Package    Version  Latest\nblack      24.0.0   24.1.0\n",
            stderr="",
        )

        passed, errors = check_outdated_packages()

        assert passed is False
        assert len(errors) == 1
        assert "Outdated packages" in errors[0]

    @patch("subprocess.run", side_effect=FileNotFoundError())
    def test_pip_not_found(self, mock_run: Mock) -> None:
        """Test when pip is not available."""
        passed, errors = check_outdated_packages()

        assert passed is False
        assert len(errors) == 1
        assert "pip not found" in errors[0]

    @patch("subprocess.run")
    def test_uses_current_python_executable(self, mock_run: Mock) -> None:
        """Test that check uses sys.executable for pip."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        check_outdated_packages()

        args, kwargs = mock_run.call_args
        assert sys.executable in args[0]
        assert "-m" in args[0]
        assert "pip" in args[0]


class TestListInstalledPackages:
    """Test list_installed_packages function."""

    @patch("subprocess.run")
    def test_list_packages_success(self, mock_run: Mock) -> None:
        """Test successful package listing."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Package    Version\nblack      24.0.0\nruff       0.6.0\n",
            stderr="",
        )

        passed, errors = list_installed_packages()

        assert passed is True
        assert len(errors) == 0

    @patch("subprocess.run", side_effect=FileNotFoundError())
    def test_list_packages_pip_not_found(self, mock_run: Mock) -> None:
        """Test package listing when pip is not available."""
        passed, errors = list_installed_packages()

        assert passed is False
        assert len(errors) == 1
        assert "pip not found" in errors[0]

    @patch("subprocess.run")
    def test_list_packages_command_construction(self, mock_run: Mock) -> None:
        """Test command construction for listing packages."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        list_installed_packages()

        args, kwargs = mock_run.call_args
        assert sys.executable in args[0]
        assert "pip" in args[0]
        assert "list" in args[0]


class TestCheckPyprojectDependencies:
    """Test check_pyproject_dependencies function."""

    @patch("subprocess.run")
    @patch("pathlib.Path.exists")
    def test_all_dependencies_installed(
        self, mock_exists: Mock, mock_run: Mock
    ) -> None:
        """Test when all required dependencies are installed."""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="black      24.0.0\nruff       0.6.0\nmypy       1.11.0\nyamllint   1.35.0\npytest     8.3.0\n",
            stderr="",
        )

        passed, errors = check_pyproject_dependencies()

        assert passed is True
        assert len(errors) == 0

    @patch("subprocess.run")
    @patch("pathlib.Path.exists")
    def test_missing_dependencies(
        self, mock_exists: Mock, mock_run: Mock
    ) -> None:
        """Test when some dependencies are missing."""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="black      24.0.0\nruff       0.6.0\n",  # Missing mypy, yamllint, pytest
            stderr="",
        )

        passed, errors = check_pyproject_dependencies()

        assert passed is False
        assert len(errors) == 1
        assert "Missing packages" in errors[0]

    @patch("pathlib.Path.exists")
    def test_no_pyproject_file(self, mock_exists: Mock) -> None:
        """Test when pyproject.toml doesn't exist."""
        mock_exists.return_value = False

        passed, errors = check_pyproject_dependencies()

        assert passed is True
        assert len(errors) == 0

    @patch("subprocess.run", side_effect=FileNotFoundError())
    @patch("pathlib.Path.exists")
    def test_pip_not_found(
        self, mock_exists: Mock, mock_run: Mock
    ) -> None:
        """Test when pip is not available."""
        mock_exists.return_value = True

        passed, errors = check_pyproject_dependencies()

        assert passed is False
        assert len(errors) == 1
        assert "pip not found" in errors[0]

    @patch("subprocess.run")
    @patch("pathlib.Path.exists")
    def test_case_insensitive_check(
        self, mock_exists: Mock, mock_run: Mock
    ) -> None:
        """Test that package checking is case-insensitive."""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Black      24.0.0\nRuff       0.6.0\nMyPy       1.11.0\nYAMLLint   1.35.0\nPyTest     8.3.0\n",
            stderr="",
        )

        passed, errors = check_pyproject_dependencies()

        assert passed is True
        assert len(errors) == 0


class TestMain:
    """Test main function."""

    @patch("python.audit.dependencies.check_pyproject_dependencies")
    @patch("python.audit.dependencies.check_outdated_packages")
    @patch("python.audit.dependencies.list_installed_packages")
    def test_main_all_pass(
        self,
        mock_list: Mock,
        mock_outdated: Mock,
        mock_deps: Mock,
    ) -> None:
        """Test main returns 0 when all checks pass."""
        mock_deps.return_value = (True, [])
        mock_outdated.return_value = (True, [])
        mock_list.return_value = (True, [])

        exit_code = main()

        assert exit_code == 0

    @patch("python.audit.dependencies.check_pyproject_dependencies")
    @patch("python.audit.dependencies.check_outdated_packages")
    @patch("python.audit.dependencies.list_installed_packages")
    def test_main_some_warnings(
        self,
        mock_list: Mock,
        mock_outdated: Mock,
        mock_deps: Mock,
    ) -> None:
        """Test main returns 1 when some checks have warnings."""
        mock_deps.return_value = (False, ["Missing packages"])
        mock_outdated.return_value = (False, ["Outdated packages"])
        mock_list.return_value = (True, [])

        exit_code = main()

        assert exit_code == 1

    @patch("python.audit.dependencies.check_pyproject_dependencies")
    @patch("python.audit.dependencies.check_outdated_packages")
    @patch("python.audit.dependencies.list_installed_packages")
    def test_main_calls_all_checks(
        self,
        mock_list: Mock,
        mock_outdated: Mock,
        mock_deps: Mock,
    ) -> None:
        """Test main calls all checks."""
        mock_deps.return_value = (True, [])
        mock_outdated.return_value = (True, [])
        mock_list.return_value = (True, [])

        main()

        mock_deps.assert_called_once()
        mock_outdated.assert_called_once()
        mock_list.assert_called_once()

    @patch("python.audit.dependencies.check_pyproject_dependencies")
    @patch("python.audit.dependencies.check_outdated_packages")
    @patch("python.audit.dependencies.list_installed_packages")
    def test_main_continues_on_failures(
        self,
        mock_list: Mock,
        mock_outdated: Mock,
        mock_deps: Mock,
    ) -> None:
        """Test main continues checking even if some fail."""
        mock_deps.return_value = (False, ["Error 1"])
        mock_outdated.return_value = (False, ["Error 2"])
        mock_list.return_value = (False, ["Error 3"])

        main()

        # All checks should be called
        mock_deps.assert_called_once()
        mock_outdated.assert_called_once()
        mock_list.assert_called_once()


class TestIntegration:
    """Integration tests for dependencies audit."""

    @patch("subprocess.run")
    def test_check_outdated_command_structure(self, mock_run: Mock) -> None:
        """Test outdated packages check uses correct command."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        check_outdated_packages()

        args, kwargs = mock_run.call_args
        assert sys.executable in args[0]
        assert "pip" in args[0]
        assert "list" in args[0]
        assert "--outdated" in args[0]

    @patch("subprocess.run")
    @patch("pathlib.Path.exists")
    def test_pyproject_check_validates_required_packages(
        self, mock_exists: Mock, mock_run: Mock
    ) -> None:
        """Test pyproject check validates all required packages."""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="black      24.0.0\n",  # Missing other required packages
            stderr="",
        )

        passed, errors = check_pyproject_dependencies()

        assert passed is False
        assert "ruff" in errors[0].lower()
        assert "mypy" in errors[0].lower()
        assert "yamllint" in errors[0].lower()
        assert "pytest" in errors[0].lower()
