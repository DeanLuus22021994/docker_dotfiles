"""
Python utilities for React Scuba project.

Enhanced for Python 3.14 with free-threaded execution,
concurrent interpreters, and improved parallelism.
"""

__version__ = "0.2.0"
__python_requires__ = ">=3.14"

# Python 3.14+ features detection
import importlib.util
import sys
from typing import Any

PYTHON_314_FEATURES = {
    "free_threaded": hasattr(sys, "_is_gil_enabled") and not sys._is_gil_enabled(),
    "interpreters": importlib.util.find_spec("concurrent.interpreters") is not None,
    "pathlib_copy_move": hasattr(__import__("pathlib").Path, "copy"),
    "tail_call_optimization": sys.version_info >= (3, 14),
}


def get_python_features() -> dict[str, Any]:
    """
    Get information about available Python 3.14+ features.

    Returns:
        dict: Dictionary of feature availability
    """
    return PYTHON_314_FEATURES.copy()


def is_free_threaded() -> bool:
    """
    Check if running in free-threaded Python mode.

    Returns:
        bool: True if GIL is disabled
    """
    return PYTHON_314_FEATURES["free_threaded"]


def has_interpreters() -> bool:
    """
    Check if concurrent interpreters are available.

    Returns:
        bool: True if concurrent.interpreters module is available
    """
    return PYTHON_314_FEATURES["interpreters"]
