"""Tests for file_utils module."""

import json
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from python.utils.file_utils import (
    ensure_dir,
    file_exists,
    get_file_size,
    get_files_by_extension,
    get_relative_path,
    read_json,
    read_lines,
    write_json,
)


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_json_file(temp_dir: Path) -> Path:
    """Create sample JSON file."""
    file_path = temp_dir / "sample.json"
    data = {"name": "test", "value": 42, "items": ["a", "b", "c"]}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return file_path


@pytest.fixture
def sample_text_file(temp_dir: Path) -> Path:
    """Create sample text file."""
    file_path = temp_dir / "sample.txt"
    content = "line1\nline2\nline3\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


class TestReadJson:
    """Test read_json function."""

    def test_read_valid_json(self, sample_json_file: Path) -> None:
        """Test reading valid JSON file."""
        result = read_json(str(sample_json_file))
        assert result["name"] == "test"
        assert result["value"] == 42
        assert result["items"] == ["a", "b", "c"]

    def test_read_nonexistent_file(self, temp_dir: Path) -> None:
        """Test reading nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            read_json(str(temp_dir / "nonexistent.json"))

    def test_read_invalid_json(self, temp_dir: Path) -> None:
        """Test reading invalid JSON raises JSONDecodeError."""
        invalid_file = temp_dir / "invalid.json"
        with open(invalid_file, "w", encoding="utf-8") as f:
            f.write("{invalid json content")

        with pytest.raises(json.JSONDecodeError):
            read_json(str(invalid_file))

    def test_read_empty_json(self, temp_dir: Path) -> None:
        """Test reading empty JSON file."""
        empty_file = temp_dir / "empty.json"
        with open(empty_file, "w", encoding="utf-8") as f:
            f.write("{}")

        result = read_json(str(empty_file))
        assert result == {}


class TestWriteJson:
    """Test write_json function."""

    def test_write_json_basic(self, temp_dir: Path) -> None:
        """Test writing JSON data."""
        file_path = temp_dir / "output.json"
        data = {"key": "value", "number": 123}

        write_json(str(file_path), data)

        assert file_path.exists()
        with open(file_path, "r", encoding="utf-8") as f:
            result = json.load(f)
        assert result == data

    def test_write_json_custom_indent(self, temp_dir: Path) -> None:
        """Test writing JSON with custom indentation."""
        file_path = temp_dir / "output.json"
        data = {"key": "value"}

        write_json(str(file_path), data, indent=4)

        content = file_path.read_text(encoding="utf-8")
        assert "    " in content  # 4 spaces indentation

    def test_write_json_complex(self, temp_dir: Path) -> None:
        """Test writing complex nested JSON."""
        file_path = temp_dir / "complex.json"
        data = {"nested": {"deep": {"value": [1, 2, 3]}}, "list": ["a", "b"]}

        write_json(str(file_path), data)

        result = read_json(str(file_path))
        assert result == data


class TestReadLines:
    """Test read_lines function."""

    def test_read_lines_strip(self, sample_text_file: Path) -> None:
        """Test reading lines with stripping."""
        result = read_lines(str(sample_text_file), strip=True)
        assert result == ["line1", "line2", "line3"]

    def test_read_lines_no_strip(self, sample_text_file: Path) -> None:
        """Test reading lines without stripping."""
        result = read_lines(str(sample_text_file), strip=False)
        assert result == ["line1\n", "line2\n", "line3\n"]

    def test_read_lines_empty_file(self, temp_dir: Path) -> None:
        """Test reading empty file."""
        empty_file = temp_dir / "empty.txt"
        empty_file.touch()

        result = read_lines(str(empty_file))
        assert result == []

    def test_read_lines_whitespace(self, temp_dir: Path) -> None:
        """Test reading lines with whitespace."""
        file_path = temp_dir / "whitespace.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("  line1  \n\n  line3  \n")

        result = read_lines(str(file_path), strip=True)
        assert result == ["line1", "", "line3"]


class TestFileExists:
    """Test file_exists function."""

    def test_file_exists_true(self, sample_json_file: Path) -> None:
        """Test file_exists returns True for existing file."""
        assert file_exists(str(sample_json_file)) is True

    def test_file_exists_false(self, temp_dir: Path) -> None:
        """Test file_exists returns False for nonexistent file."""
        assert file_exists(str(temp_dir / "nonexistent.txt")) is False

    def test_file_exists_directory(self, temp_dir: Path) -> None:
        """Test file_exists returns True for directory."""
        assert file_exists(str(temp_dir)) is True


class TestEnsureDir:
    """Test ensure_dir function."""

    def test_ensure_dir_create(self, temp_dir: Path) -> None:
        """Test creating new directory."""
        new_dir = temp_dir / "new_directory"
        ensure_dir(str(new_dir))
        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_ensure_dir_exists(self, temp_dir: Path) -> None:
        """Test ensuring existing directory doesn't fail."""
        ensure_dir(str(temp_dir))
        assert temp_dir.exists()

    def test_ensure_dir_nested(self, temp_dir: Path) -> None:
        """Test creating nested directories."""
        nested_dir = temp_dir / "level1" / "level2" / "level3"
        ensure_dir(str(nested_dir))
        assert nested_dir.exists()
        assert nested_dir.is_dir()


class TestGetFilesByExtension:
    """Test get_files_by_extension function."""

    def test_get_files_recursive(self, temp_dir: Path) -> None:
        """Test getting files recursively."""
        (temp_dir / "file1.py").touch()
        (temp_dir / "file2.txt").touch()
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "file3.py").touch()

        result = get_files_by_extension(str(temp_dir), ".py", recursive=True)
        assert len(result) == 2

    def test_get_files_non_recursive(self, temp_dir: Path) -> None:
        """Test getting files non-recursively."""
        (temp_dir / "file1.py").touch()
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "file2.py").touch()

        result = get_files_by_extension(str(temp_dir), ".py", recursive=False)
        assert len(result) == 1

    def test_get_files_extension_format(self, temp_dir: Path) -> None:
        """Test extension with and without dot."""
        (temp_dir / "file.json").touch()

        result1 = get_files_by_extension(str(temp_dir), ".json")
        result2 = get_files_by_extension(str(temp_dir), "json")
        assert len(result1) == len(result2) == 1

    def test_get_files_no_matches(self, temp_dir: Path) -> None:
        """Test getting files with no matches."""
        (temp_dir / "file.txt").touch()

        result = get_files_by_extension(str(temp_dir), ".py")
        assert len(result) == 0


class TestGetFileSize:
    """Test get_file_size function."""

    def test_get_file_size_basic(self, temp_dir: Path) -> None:
        """Test getting file size."""
        file_path = temp_dir / "sized.txt"
        content = "test content"
        file_path.write_text(content, encoding="utf-8")

        result = get_file_size(str(file_path))
        assert result == len(content.encode("utf-8"))

    def test_get_file_size_empty(self, temp_dir: Path) -> None:
        """Test getting size of empty file."""
        file_path = temp_dir / "empty.txt"
        file_path.touch()

        result = get_file_size(str(file_path))
        assert result == 0


class TestGetRelativePath:
    """Test get_relative_path function."""

    def test_get_relative_path_basic(self, temp_dir: Path) -> None:
        """Test getting relative path."""
        file_path = temp_dir / "subdir" / "file.txt"
        file_path.parent.mkdir(parents=True, exist_ok=True)

        result = get_relative_path(str(file_path), str(temp_dir))
        assert "subdir" in result
        assert "file.txt" in result

    def test_get_relative_path_same_dir(self, temp_dir: Path) -> None:
        """Test relative path in same directory."""
        file_path = temp_dir / "file.txt"

        result = get_relative_path(str(file_path), str(temp_dir))
        assert result == "file.txt"
