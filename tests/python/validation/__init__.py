"""Validation module tests.

Tests for scripts/python/validation/ module covering:
    - validate_configs.py - YAML, JSON, nginx, PostgreSQL, MariaDB config validation
    - validate_env.py - Environment variable validation and .env file checking

Test Coverage:
    - 47 tests for validation module functionality
    - Mocked subprocess and file system interactions
    - Edge case handling (missing files, invalid formats, empty values)
"""

__all__: list[str] = []
