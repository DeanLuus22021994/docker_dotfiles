"""
Python Scripts Package

Root package for all Python automation scripts organized by functionality.
Follows SRP (Single Responsibility Principle) and DRY (Don't Repeat Yourself)
principles for maintainable, enterprise-grade code.

Subpackages:
    audit: Code quality auditing and dependency management
    validation: Environment and configuration validation
    utils: Shared utilities (colors, file operations, logging)

Examples:
    >>> from python.audit import code_quality
    >>> from python.validation import validate_env
    >>> from python.utils.colors import success

Version:
    Python 3.14+ compatible
    Last updated: 2025-10-25
"""

from . import audit, utils, validation

__all__: list[str] = ["audit", "utils", "validation"]
