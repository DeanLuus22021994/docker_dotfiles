"""
Python Validation Package

Provides comprehensive validation tools for environment variables and
configuration files using modular validator classes. Each validation type
is handled by dedicated classes following the Single Responsibility Principle.

Modules:
    validate_configs: Validates configs with ConfigurationAuditor
    validate_env: Validates environment variables with EnvValidator

Examples:
    >>> from python.validation import EnvValidator, ConfigurationAuditor
    >>> validator = EnvValidator()
    >>> result = validator.validate()
    >>> print(result.is_valid)

See Also:
    - scripts/orchestrator.py validate env
    - scripts/orchestrator.py validate configs
"""

# Import submodules to make them available in the package namespace
from . import validate_configs, validate_env

# Import class-based APIs
from .validate_configs import (
    BaseConfigValidator,
    ConfigurationAuditor,
    JsonValidator,
    MARIADB_CONFIG,
    MariadbValidator,
    NGINX_CONFIGS,
    NginxValidator,
    POSTGRESQL_CONFIG,
    PostgresqlValidator,
    ValidationReport,
    ValidationResult,
    YAML_LINE_LENGTH,
    YamlValidator,
    main as configs_main,
)
from .validate_env import (
    EnvVarConfig,
    EnvValidator,
    MASK_LENGTH,
    MASK_SUFFIX,
    OPTIONAL_ENV_VARS,
    REQUIRED_ENV_VARS,
    SHORT_MASK,
    ValidationReporter,
    ValidationResult as EnvValidationResult,
    main as env_main,
)

__all__: list[str] = [
    # Submodules
    "validate_configs",
    "validate_env",
    # Config validation classes and constants
    "ConfigurationAuditor",
    "BaseConfigValidator",
    "YamlValidator",
    "JsonValidator",
    "NginxValidator",
    "PostgresqlValidator",
    "MariadbValidator",
    "ValidationResult",
    "ValidationReport",
    "YAML_LINE_LENGTH",
    "NGINX_CONFIGS",
    "POSTGRESQL_CONFIG",
    "MARIADB_CONFIG",
    "configs_main",
    # Env validation classes and constants
    "EnvValidator",
    "ValidationReporter",
    "EnvVarConfig",
    "EnvValidationResult",
    "REQUIRED_ENV_VARS",
    "OPTIONAL_ENV_VARS",
    "MASK_LENGTH",
    "MASK_SUFFIX",
    "SHORT_MASK",
    "env_main",
]
