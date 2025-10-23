"""
React Scuba Utils - Modular enterprise-grade MCP-compliant Python utilities.

This package provides comprehensive documentation utilities for React Scuba projects,
including link checking, component inventory generation, and file operations.

Features:
- Python 3.14+ free-threaded execution support
- Concurrent interpreters for true parallelism
- MCP (Model Context Protocol) server integration
- Type-safe implementations with Pydantic
- Precompiled optimizations with mypyc
- Modular architecture under 300 lines per module

Usage:
    from react_scuba_utils import DocUtils

    utils = DocUtils()
    results = utils.check_links_concurrent()
    inventory = utils.generate_component_inventory()
"""

from .config.settings import get_python_features, has_interpreters, is_free_threaded
from .core.utils import DocUtils

__version__ = "0.2.0"
__author__ = "React Scuba Team"
__email__ = "team@react-scuba.dev"

# Feature detection
PYTHON_FEATURES = get_python_features()

__all__ = [
    "DocUtils",
    "get_python_features",
    "is_free_threaded",
    "has_interpreters",
    "PYTHON_FEATURES",
]
