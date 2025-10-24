"""
Python utilities for Docker Compose Utils project.
"""

# Python 3.14+ features detection
import importlib.util
import sys
from typing import Any

from .docker_examples_utils.models import ComponentInfo, LinkResult
from .docker_examples_utils.services import (
    ComponentInventoryService,
    LinkCheckerService,
)

__all__ = [
    "get_python_features",
    "is_free_threaded",
    "has_interpreters",
    "ComponentInfo",
    "LinkResult",
    "ComponentInventoryService",
    "LinkCheckerService",
]
