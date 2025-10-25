"""Python module tests.

Mirrors the structure of scripts/python/ for organized test discovery.

Subpackages:
    audit - Tests for audit module (code_quality, dependencies)
    utils - Tests for utils module (colors, file_utils, logging_utils)
    validation - Tests for validation module (validate_env, validate_configs)

All tests use pytest patterns with dependency injection via fixtures.
"""

__all__: list[str] = []
