"""
Python Validation Package

Provides comprehensive validation tools for environment variables and
configuration files. Ensures all required settings are present and valid
before Docker stack deployment.

Modules:
    validate_configs: Validates YAML, JSON, nginx, PostgreSQL, and MariaDB configs
    validate_env: Validates required and optional environment variables

Examples:
    >>> from python.validation import validate_env, validate_configs
    >>> from python.validation import *  # Exports via __all__

See Also:
    - scripts/orchestrator.py validate env
    - scripts/orchestrator.py validate configs
"""

# Import submodules to make them available in the package namespace
from . import validate_configs, validate_env

__all__: list[str] = ["validate_configs", "validate_env"]
