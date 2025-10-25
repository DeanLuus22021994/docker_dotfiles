"""
Python Validation Package

Provides comprehensive validation tools for environment variables and
configuration files. Ensures all required settings are present and valid
before Docker stack deployment.

Modules:
    validate_configs: Validates YAML, JSON, nginx, PostgreSQL, and MariaDB configs
    validate_env: Validates required and optional environment variables

Examples:
    >>> from python.validation import validate_env_vars, validate_yaml_files
    >>> from python.validation import *  # Exports via __all__

See Also:
    - scripts/orchestrator.py validate env
    - scripts/orchestrator.py validate configs
"""

# Import submodules to make them available in the package namespace
from . import validate_configs, validate_env
from .validate_configs import (
    main as configs_main,
    validate_json_files,
    validate_mariadb_config,
    validate_nginx_configs,
    validate_postgresql_config,
    validate_yaml_files,
)
from .validate_env import (
    main as env_main,
    print_summary,
    validate_env_vars,
)

__all__: list[str] = [
    # Submodules
    "validate_configs",
    "validate_env",
    # Config validation functions
    "validate_yaml_files",
    "validate_json_files",
    "validate_nginx_configs",
    "validate_postgresql_config",
    "validate_mariadb_config",
    "configs_main",
    # Env validation functions
    "validate_env_vars",
    "print_summary",
    "env_main",
]
