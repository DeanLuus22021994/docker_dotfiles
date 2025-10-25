"""Test suite for docker-modern-data-platform.

Comprehensive pytest-based test suite with 143 tests achieving 97.05% coverage.
Tests all Python modules under scripts/python/ directory structure.

Test Organization:
    - tests/python/audit/ - Code quality and dependency management tests
    - tests/python/utils/ - Utility module tests (colors, file_utils, logging)
    - tests/python/validation/ - Configuration and environment validation tests

Framework:
    pytest 8.3+ with pytest-cov, pytest-mock, pytest-asyncio plugins

Python Version:
    3.14.0 with modern type hints (PEP 585, PEP 604)

See:
    tests/README.md - Complete test suite documentation
    tests/conftest.py - Shared pytest fixtures
"""

__all__: list[str] = []
