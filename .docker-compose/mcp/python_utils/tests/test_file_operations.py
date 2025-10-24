"""
Unit tests for FileOperationsService.

Comprehensive test coverage for file operations functionality,
including copy, move, create, remove, and info operations.
"""

from pathlib import Path
from unittest.mock import patch

import pytest

from docker_examples_utils.services.file_operations import FileOperationsService


class TestFileOperationsService:
    """Test suite for FileOperationsService."""

    @pytest.fixture
    def service(self) -> FileOperationsService:
        """Create FileOperationsService instance."""
        return FileOperationsService()

    @pytest.fixture
    def temp_files(self, tmp_path: Path) -> dict[str, Path]:
        """Create temporary test files."""
        src_file = tmp_path / "source.txt"
        dst_file = tmp_path / "dest.txt"
        src_dir = tmp_path / "src_dir"
        dst_dir = tmp_path / "dst_dir"

        src_file.write_text("test content")
        src_dir.mkdir()

        return {
            "src_file": src_file,
            "dst_file": dst_file,
            "src_dir": src_dir,
            "dst_dir": dst_dir,
        }

    def test_copy_file_python_314(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test file copying with Python 3.14+ copy method."""
        src_file = temp_files["src_file"]
        dst_file = temp_files["dst_file"]

        # Mock the copy method to simulate Python 3.14+
        with patch.object(Path, 'copy') as mock_copy:
            result = service.copy_file(src_file, dst_file)

        assert result is True
        mock_copy.assert_called_once_with(dst_file, follow_symlinks=True)

    def test_copy_file_fallback(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test file copying with shutil fallback."""
        src_file = temp_files["src_file"]
        dst_file = temp_files["dst_file"]

        # Mock no copy method (older Python)
        with patch.object(Path, 'copy', side_effect=AttributeError):
            with patch('shutil.copy2') as mock_copy2:
                result = service.copy_file(src_file, dst_file)

        assert result is True
        mock_copy2.assert_called_once_with(src_file, dst_file, follow_symlinks=True)

    def test_copy_file_error(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test file copying error handling."""
        src_file = temp_files["src_file"]
        dst_file = temp_files["dst_file"]

        with patch.object(Path, 'copy', side_effect=PermissionError("Access denied")):
            result = service.copy_file(src_file, dst_file)

        assert result is False

    def test_copy_file_with_path_objects(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test file copying with Path objects."""
        src_file = temp_files["src_file"]
        dst_file = temp_files["dst_file"]

        with patch.object(Path, 'copy') as mock_copy:
            result = service.copy_file(src_file, dst_file, follow_symlinks=False)

        assert result is True
        mock_copy.assert_called_once_with(dst_file, follow_symlinks=False)

    def test_move_file_python_314(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test file moving with Python 3.14+ move method."""
        src_file = temp_files["src_file"]
        dst_file = temp_files["dst_file"]

        with patch.object(Path, 'move') as mock_move:
            result = service.move_file(src_file, dst_file)

        assert result is True
        mock_move.assert_called_once_with(dst_file)

    def test_move_file_fallback(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test file moving with shutil fallback."""
        src_file = temp_files["src_file"]
        dst_file = temp_files["dst_file"]

        with patch.object(Path, 'move', side_effect=AttributeError):
            with patch('shutil.move') as mock_move:
                result = service.move_file(src_file, dst_file)

        assert result is True
        mock_move.assert_called_once_with(src_file, dst_file)

    def test_move_file_error(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test file moving error handling."""
        src_file = temp_files["src_file"]
        dst_file = temp_files["dst_file"]

        with patch.object(Path, 'move', side_effect=OSError("Move failed")):
            result = service.move_file(src_file, dst_file)

        assert result is False

    def test_create_directory_success(self, service: FileOperationsService, tmp_path: Path):
        """Test successful directory creation."""
        new_dir = tmp_path / "new_directory"

        result = service.create_directory(new_dir)

        assert result is True
        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_create_directory_with_parents(self, service: FileOperationsService, tmp_path: Path):
        """Test directory creation with parent directories."""
        nested_dir = tmp_path / "parent" / "child" / "grandchild"

        result = service.create_directory(nested_dir, parents=True)

        assert result is True
        assert nested_dir.exists()
        assert nested_dir.is_dir()

    def test_create_directory_exists_error(self, service: FileOperationsService, tmp_path: Path):
        """Test directory creation when directory exists and exist_ok=False."""
        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()

        result = service.create_directory(existing_dir, exist_ok=False)

        assert result is False

    def test_create_directory_permission_error(self, service: FileOperationsService, tmp_path: Path):
        """Test directory creation permission error."""
        protected_dir = tmp_path / "protected" / "nested"

        with patch.object(Path, 'mkdir', side_effect=PermissionError("Permission denied")):
            result = service.create_directory(protected_dir)

        assert result is False

    def test_remove_file_python_314(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test file removal with Python 3.14+ unlink method."""
        src_file = temp_files["src_file"]

        with patch.object(Path, 'unlink') as mock_unlink:
            result = service.remove_file(src_file)

        assert result is True
        mock_unlink.assert_called_once_with(missing_ok=True)

    def test_remove_file_fallback(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test file removal with fallback for older Python."""
        src_file = temp_files["src_file"]

        with patch.object(Path, 'unlink', side_effect=AttributeError):
            with patch.object(Path, 'exists', return_value=True):
                with patch.object(Path, 'unlink') as mock_unlink:
                    result = service.remove_file(src_file)

        assert result is True
        mock_unlink.assert_called_once()

    def test_remove_file_missing_ok_false(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test file removal when file doesn't exist and missing_ok=False."""
        missing_file = temp_files["dst_file"]  # Doesn't exist

        with patch.object(Path, 'exists', return_value=False):
            result = service.remove_file(missing_file, missing_ok=False)

        assert result is False

    def test_remove_file_error(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test file removal error handling."""
        src_file = temp_files["src_file"]

        with patch.object(Path, 'unlink', side_effect=OSError("Remove failed")):
            result = service.remove_file(src_file)

        assert result is False

    def test_get_file_info_existing_file(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test getting file information for existing file."""
        src_file = temp_files["src_file"]

        info = service.get_file_info(src_file)

        assert info["path"] == str(src_file)
        assert info["name"] == "source.txt"
        assert info["stem"] == "source"
        assert info["suffix"] == ".txt"
        assert info["size"] == 12  # "test content" is 12 bytes
        assert info["exists"] is True
        assert info["is_file"] is True
        assert info["is_dir"] is False
        assert info["is_symlink"] is False
        assert "modified" in info
        assert "created" in info

    def test_get_file_info_directory(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test getting file information for directory."""
        src_dir = temp_files["src_dir"]

        info = service.get_file_info(src_dir)

        assert info["path"] == str(src_dir)
        assert info["name"] == "src_dir"
        assert info["exists"] is True
        assert info["is_file"] is False
        assert info["is_dir"] is True
        assert info["is_symlink"] is False

    def test_get_file_info_nonexistent(self, service: FileOperationsService, tmp_path: Path):
        """Test getting file information for nonexistent file."""
        nonexistent = tmp_path / "nonexistent.txt"

        info = service.get_file_info(nonexistent)

        assert info["path"] == str(nonexistent)
        assert info["exists"] is False
        assert "error" in info

    def test_get_file_info_error(self, service: FileOperationsService, temp_files: dict[str, Path]):
        """Test file info error handling."""
        src_file = temp_files["src_file"]

        with patch.object(Path, 'stat', side_effect=PermissionError("Access denied")):
            info = service.get_file_info(src_file)

        assert info["path"] == str(src_file)
        assert info["exists"] is False
        assert "error" in info
        assert "Access denied" in info["error"]

    def test_get_file_info_symlink(self, service: FileOperationsService, temp_files: dict[str, Path], tmp_path: Path):
        """Test getting file information for symlink."""
        src_file = temp_files["src_file"]
        link_file = tmp_path / "link.txt"

        # Create symlink if supported
        try:
            link_file.symlink_to(src_file)
            info = service.get_file_info(link_file)

            assert info["path"] == str(link_file)
            assert info["is_symlink"] is True
        except (OSError, NotImplementedError):
            # Symlinks not supported on this platform
            pytest.skip("Symlinks not supported on this platform")

    def test_string_path_conversion(self, service: FileOperationsService, tmp_path: Path):
        """Test that string paths are properly converted to Path objects."""
        src_str = str(tmp_path / "test.txt")
        dst_str = str(tmp_path / "copy.txt")

        # Create source file
        Path(src_str).write_text("test")

        with patch.object(Path, 'copy') as mock_copy:
            result = service.copy_file(src_str, dst_str)

        assert result is True
        # Verify Path objects were created and used
        mock_copy.assert_called_once()