"""Tests for code_quality module."""

from unittest.mock import Mock, patch

import pytest

from scripts.python.audit.code_quality import (
    BlackChecker,
    CodeQualityAuditor,
    MypyChecker,
    RuffChecker,
    main,
    run_black_check,
    run_mypy_check,
    run_ruff_check,
)


class TestRunBlackCheck:
    """Test run_black_check function."""

    @patch("subprocess.run")
    def test_black_check_success(self, mock_run: Mock) -> None:
        """Test successful Black format check."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        passed, errors = run_black_check()

        assert passed is True
        assert len(errors) == 0
        mock_run.assert_called_once()
        assert "black" in str(mock_run.call_args)

    @patch("subprocess.run")
    def test_black_check_failure(self, mock_run: Mock) -> None:
        """Test Black format check with formatting issues."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="would reformat scripts/python/utils/colors.py",
            stderr="",
        )

        passed, errors = run_black_check()

        assert passed is False
        assert len(errors) == 1
        assert "Black formatting issues" in errors[0]

    @patch("subprocess.run", side_effect=FileNotFoundError())
    def test_black_check_not_installed(self, mock_run: Mock) -> None:
        """Test Black check when Black is not installed."""
        passed, errors = run_black_check()

        assert passed is False
        assert len(errors) == 1
        assert "Black not found" in errors[0]


class TestRunRuffCheck:
    """Test run_ruff_check function."""

    @patch("subprocess.run")
    def test_ruff_check_success(self, mock_run: Mock) -> None:
        """Test successful Ruff linting check."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        passed, errors = run_ruff_check()

        assert passed is True
        assert len(errors) == 0
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_ruff_check_failure(self, mock_run: Mock) -> None:
        """Test Ruff check with linting issues."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="scripts/python/utils/colors.py:10:1: E501 line too long",
            stderr="",
        )

        passed, errors = run_ruff_check()

        assert passed is False
        assert len(errors) == 1
        assert "Ruff found linting issues" in errors[0]

    @patch("subprocess.run", side_effect=FileNotFoundError())
    def test_ruff_check_not_installed(self, mock_run: Mock) -> None:
        """Test Ruff check when Ruff is not installed."""
        passed, errors = run_ruff_check()

        assert passed is False
        assert len(errors) == 1
        assert "Ruff not found" in errors[0]


class TestRunMypyCheck:
    """Test run_mypy_check function."""

    @patch("subprocess.run")
    def test_mypy_check_success(self, mock_run: Mock) -> None:
        """Test successful mypy type check."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        passed, errors = run_mypy_check()

        assert passed is True
        assert len(errors) == 0
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_mypy_check_failure(self, mock_run: Mock) -> None:
        """Test mypy check with type errors."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="scripts/python/utils/colors.py:10: error: Incompatible types",
            stderr="",
        )

        passed, errors = run_mypy_check()

        assert passed is False
        assert len(errors) == 1
        assert "mypy found type errors" in errors[0]

    @patch("subprocess.run", side_effect=FileNotFoundError())
    def test_mypy_check_not_installed(self, mock_run: Mock) -> None:
        """Test mypy check when mypy is not installed."""
        passed, errors = run_mypy_check()

        assert passed is False
        assert len(errors) == 1
        assert "mypy not found" in errors[0]


class TestMain:
    """Test main function."""

    @patch("python.audit.code_quality.run_black_check")
    @patch("python.audit.code_quality.run_ruff_check")
    @patch("python.audit.code_quality.run_mypy_check")
    def test_main_all_pass(
        self,
        mock_mypy: Mock,
        mock_ruff: Mock,
        mock_black: Mock,
    ) -> None:
        """Test main returns 0 when all checks pass."""
        mock_black.return_value = (True, [])
        mock_ruff.return_value = (True, [])
        mock_mypy.return_value = (True, [])

        exit_code = main()

        assert exit_code == 0
        mock_black.assert_called_once()
        mock_ruff.assert_called_once()
        mock_mypy.assert_called_once()

    @patch("python.audit.code_quality.run_black_check")
    @patch("python.audit.code_quality.run_ruff_check")
    @patch("python.audit.code_quality.run_mypy_check")
    def test_main_some_fail(
        self,
        mock_mypy: Mock,
        mock_ruff: Mock,
        mock_black: Mock,
    ) -> None:
        """Test main returns 1 when some checks fail."""
        mock_black.return_value = (True, [])
        mock_ruff.return_value = (False, ["Ruff error"])
        mock_mypy.return_value = (False, ["mypy error"])

        exit_code = main()

        assert exit_code == 1

    @patch("python.audit.code_quality.run_black_check")
    @patch("python.audit.code_quality.run_ruff_check")
    @patch("python.audit.code_quality.run_mypy_check")
    def test_main_all_fail(
        self,
        mock_mypy: Mock,
        mock_ruff: Mock,
        mock_black: Mock,
    ) -> None:
        """Test main returns 1 when all checks fail."""
        mock_black.return_value = (False, ["Black error"])
        mock_ruff.return_value = (False, ["Ruff error"])
        mock_mypy.return_value = (False, ["mypy error"])

        exit_code = main()

        assert exit_code == 1

    @patch("python.audit.code_quality.run_black_check")
    @patch("python.audit.code_quality.run_ruff_check")
    @patch("python.audit.code_quality.run_mypy_check")
    def test_main_calls_all_checks(
        self,
        mock_mypy: Mock,
        mock_ruff: Mock,
        mock_black: Mock,
    ) -> None:
        """Test main calls all checks regardless of failures."""
        mock_black.return_value = (False, ["Black error"])
        mock_ruff.return_value = (False, ["Ruff error"])
        mock_mypy.return_value = (False, ["mypy error"])

        main()

        # All checks should be called even if some fail
        mock_black.assert_called_once()
        mock_ruff.assert_called_once()
        mock_mypy.assert_called_once()


class TestIntegration:
    """Integration tests for code quality checks."""

    @patch("subprocess.run")
    def test_black_check_with_real_command(self, mock_run: Mock) -> None:
        """Test Black check with realistic command construction."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        run_black_check()

        args, kwargs = mock_run.call_args
        assert "black" in args[0]
        assert "--check" in args[0]
        assert "--line-length=100" in args[0]

    @patch("subprocess.run")
    def test_ruff_check_with_real_command(self, mock_run: Mock) -> None:
        """Test Ruff check with realistic command construction."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        run_ruff_check()

        args, kwargs = mock_run.call_args
        assert "ruff" in args[0]
        assert "check" in args[0]

    @patch("subprocess.run")
    def test_mypy_check_with_real_command(self, mock_run: Mock) -> None:
        """Test mypy check with realistic command construction."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        run_mypy_check()

        args, kwargs = mock_run.call_args
        assert "mypy" in args[0]
        assert "--strict" in args[0]
