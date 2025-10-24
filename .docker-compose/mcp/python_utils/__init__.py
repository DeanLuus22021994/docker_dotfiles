"""
Python utilities for Docker Compose Utils project.
"""

# Python 3.14+ features detection
import importlib.util
import sys
from typing import Any

def _check_free_threaded() -> bool:
    """Check if running in free-threaded mode safely."""
    try:
        return hasattr(sys, "_is_gil_enabled") and not getattr(sys, "_is_gil_enabled", True)
    except AttributeError:
        return False

PYTHON_314_FEATURES = {
    "free_threaded": _check_free_threaded(),
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


# Re-export main classes from docker_examples_utils for convenience
from .docker_examples_utils.models import ComponentInfo, LinkResult
from .docker_examples_utils.services import ComponentInventoryService, LinkCheckerService

__all__ = [
    "get_python_features",
    "is_free_threaded",
    "has_interpreters",
    "ComponentInfo",
    "LinkResult",
    "ComponentInventoryService",
    "LinkCheckerService",
]
