"""Configuration management and settings."""

from .config import (
    ApplicationConfig,
    DatabaseConfig,
    Environment,
    HTTPConfig,
    LoggingConfig,
    LogLevel,
    PathConfig,
    RedisConfig,
    ServiceConfig,
    get_config,
    get_database_config,
    get_http_config,
    get_logging_config,
    get_path_config,
    get_redis_config,
    reload_config,
    validate_config,
)
from .settings import (
    CorrelationLogger,
    get_python_features,
    has_interpreters,
    is_free_threaded,
)
from .settings import (
    HTTPConfig as LegacyHTTPConfig,
)
from .settings import (
    LoggingConfig as LegacyLoggingConfig,
)
from .settings import (
    PathConfig as LegacyPathConfig,
)

__all__ = [
    # New centralized config
    "ApplicationConfig",
    "DatabaseConfig",
    "RedisConfig",
    "HTTPConfig",
    "PathConfig",
    "LoggingConfig",
    "ServiceConfig",
    "Environment",
    "LogLevel",
    "get_config",
    "reload_config",
    "validate_config",
    "get_database_config",
    "get_redis_config",
    "get_http_config",
    "get_path_config",
    "get_logging_config",
    # Legacy compatibility
    "LegacyLoggingConfig",
    "LegacyHTTPConfig",
    "LegacyPathConfig",
    "CorrelationLogger",
    "get_python_features",
    "is_free_threaded",
    "has_interpreters",
]
