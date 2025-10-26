"""Test fixtures package.

This package contains shared test fixtures that are automatically available
to all test modules through pytest plugin registration in conftest.py.

Available fixtures:
- temp_dir: Temporary directory for file operations
- temp_project_dir: Project structure with .config/nginx and .config/database
- sample_json_file: JSON file with test data
- sample_text_file: Text file with three lines
- clean_env: Clean environment variables before/after tests
- cleanup_loggers: Reset all loggers after tests

Import fixtures directly in tests without explicit imports:

    def test_something(temp_dir: Path) -> None:
        test_file = temp_dir / "test.txt"
        test_file.write_text("content")

See common.py for detailed fixture documentation.
"""

__all__ = [
    "clean_env",
    "cleanup_loggers",
    "sample_json_file",
    "sample_text_file",
    "temp_dir",
    "temp_project_dir",
]
