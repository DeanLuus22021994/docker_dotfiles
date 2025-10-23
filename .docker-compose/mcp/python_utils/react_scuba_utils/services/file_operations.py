"""
File operations service for React Scuba utilities.

This module provides enhanced file operations with support for
Python 3.14+ pathlib improvements.
"""

import sys
from pathlib import Path
from typing import Any


class FileOperationsService:
    """
    Service for file operations with Python 3.14+ enhancements.

    Provides copy and move operations using pathlib's native methods
    when available, with fallbacks for older Python versions.
    """

    def copy_file(
        self, src: str | Path, dst: str | Path, follow_symlinks: bool = True
    ) -> bool:
        """
        Copy a file using pathlib's copy method (Python 3.14+).

        Falls back to shutil for older versions.

        Args:
            src: Source file path
            dst: Destination file path
            follow_symlinks: Whether to follow symbolic links

        Returns:
            True if successful, False otherwise
        """
        src_path = Path(src)
        dst_path = Path(dst)

        try:
            if hasattr(src_path, "copy"):  # Python 3.14+
                src_path.copy(dst_path, follow_symlinks=follow_symlinks)
            else:
                # Fallback to shutil
                import shutil

                shutil.copy2(src_path, dst_path, follow_symlinks=follow_symlinks)
            return True
        except Exception as e:
            print(f"Error copying {src_path} to {dst_path}: {e}", file=sys.stderr)
            return False

    def move_file(self, src: str | Path, dst: str | Path) -> bool:
        """
        Move a file using pathlib's move method (Python 3.14+).

        Falls back to shutil for older versions.

        Args:
            src: Source file path
            dst: Destination file path

        Returns:
            True if successful, False otherwise
        """
        src_path = Path(src)
        dst_path = Path(dst)

        try:
            if hasattr(src_path, "move"):  # Python 3.14+
                src_path.move(dst_path)
            else:
                # Fallback to shutil
                import shutil

                shutil.move(src_path, dst_path)
            return True
        except Exception as e:
            print(f"Error moving {src_path} to {dst_path}: {e}", file=sys.stderr)
            return False

    def create_directory(
        self, path: str | Path, parents: bool = True, exist_ok: bool = True
    ) -> bool:
        """
        Create a directory with pathlib.

        Args:
            path: Directory path to create
            parents: Create parent directories if needed
            exist_ok: Don't raise error if directory exists

        Returns:
            True if successful, False otherwise
        """
        dir_path = Path(path)

        try:
            dir_path.mkdir(parents=parents, exist_ok=exist_ok)
            return True
        except Exception as e:
            print(f"Error creating directory {dir_path}: {e}", file=sys.stderr)
            return False

    def remove_file(self, path: str | Path, missing_ok: bool = True) -> bool:
        """
        Remove a file safely.

        Args:
            path: File path to remove
            missing_ok: Don't raise error if file doesn't exist

        Returns:
            True if successful, False otherwise
        """
        file_path = Path(path)

        try:
            if hasattr(file_path, "unlink"):  # Python 3.14+
                file_path.unlink(missing_ok=missing_ok)
            else:
                # Fallback for older versions
                if file_path.exists():
                    file_path.unlink()
                elif not missing_ok:
                    raise FileNotFoundError(f"No such file: {file_path}")
            return True
        except Exception as e:
            print(f"Error removing {file_path}: {e}", file=sys.stderr)
            return False

    def get_file_info(self, path: str | Path) -> dict[str, Any]:
        """
        Get comprehensive file information.

        Args:
            path: File path to analyze

        Returns:
            Dictionary with file information
        """
        file_path = Path(path)

        try:
            stat = file_path.stat()
            return {
                "path": str(file_path),
                "name": file_path.name,
                "stem": file_path.stem,
                "suffix": file_path.suffix,
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "created": stat.st_ctime,
                "exists": file_path.exists(),
                "is_file": file_path.is_file(),
                "is_dir": file_path.is_dir(),
                "is_symlink": file_path.is_symlink(),
            }
        except Exception as e:
            print(f"Error getting info for {file_path}: {e}", file=sys.stderr)
            return {
                "path": str(file_path),
                "error": str(e),
                "exists": False,
            }
