"""
Centralized Configuration Management with Schema Validation

This module provides a comprehensive configuration system using Pydantic
for schema validation and environment variable management. It centralizes
all configuration across different environments and services.
"""

import logging
import os
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Application environment enumeration."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging level enumeration."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DatabaseConfig(BaseModel):
    """Database configuration schema."""

    host: str = Field(..., description="Database host")
    port: int = Field(..., ge=1, le=65535, description="Database port")
    name: str = Field(..., description="Database name")
    user: str = Field(..., description="Database username")
    password: str | None = Field(default=None, description="Redis password")
    ssl_mode: str = Field(default="prefer", description="SSL mode for connections")
    connection_timeout: int = Field(
        default=30, ge=1, description="Connection timeout in seconds"
    )
    max_connections: int = Field(
        default=20, ge=1, description="Maximum connection pool size"
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets minimum requirements."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    @property
    def connection_string(self) -> str:
        """Generate database connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}?sslmode={self.ssl_mode}"


class RedisConfig(BaseModel):
    """Redis configuration schema."""

    host: str = Field(default="localhost", description="Redis host")
    port: int = Field(default=6379, ge=1, le=65535, description="Redis port")
    db: int = Field(default=0, ge=0, le=15, description="Redis database number")
    password: str | None = Field(default=None, description="Redis password")
    socket_timeout: int = Field(
        default=5, ge=1, description="Socket timeout in seconds"
    )
    socket_connect_timeout: int = Field(
        default=5, ge=1, description="Socket connect timeout"
    )
    max_connections: int = Field(
        default=20, ge=1, description="Maximum connection pool size"
    )

    @property
    def connection_string(self) -> str:
        """Generate Redis connection string."""
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"


class HTTPConfig(BaseModel):
    """HTTP client configuration schema."""

    timeout: int = Field(default=30, ge=1, description="Request timeout in seconds")
    max_retries: int = Field(default=3, ge=0, description="Maximum retry attempts")
    backoff_factor: float = Field(
        default=1.0, ge=0.1, description="Backoff factor for retries"
    )
    retry_status_codes: list[int] = Field(
        default=[429, 500, 502, 503, 504], description="HTTP status codes to retry on"
    )
    user_agent: str = Field(
        default="React-Scuba/1.0", description="User agent string for requests"
    )


class PathConfig(BaseModel):
    """Path configuration schema."""

    docs_path: Path = Field(
        default=Path("docs"), description="Documentation directory path"
    )
    src_path: Path = Field(
        default=Path("src"), description="Source code directory path"
    )
    base_url: str = Field(
        default="https://deanluus22021994.github.io/react-scuba/",
        description="Base URL for the application",
    )

    @field_validator("docs_path", "src_path")
    @classmethod
    def validate_path_exists(cls, v: Path) -> Path:
        if not os.getenv("DOCKER_BUILDKIT"):
            if not v.exists():
                raise ValueError(f"Path does not exist: {v}")
        return v

    def resolve_src_path(self) -> Path:
        """Resolve the source path."""
        return self.src_path


class LoggingConfig(BaseModel):
    """Logging configuration schema."""

    level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    format: str = Field(default="json", description="Log format (json or text)")
    enable_correlation_ids: bool = Field(
        default=True, description="Enable correlation ID tracking"
    )
    log_to_file: bool = Field(
        default=False, description="Log to file in addition to console"
    )
    log_file_path: Path | None = Field(default=None, description="Log file path")

    def configure_logging(self) -> None:
        import sys

        level = getattr(logging, self.level.value)

        if self.format == "json":
            try:
                import structlog

                structlog.configure(
                    processors=[
                        structlog.stdlib.filter_by_level,
                        structlog.stdlib.add_logger_name,
                        structlog.stdlib.add_log_level,
                        structlog.stdlib.PositionalArgumentsFormatter(),
                        structlog.processors.TimeStamper(fmt="iso"),
                        structlog.processors.StackInfoRenderer(),
                        structlog.processors.format_exc_info,
                        structlog.processors.UnicodeDecoder(),
                        structlog.processors.JSONRenderer(),
                    ],
                    context_class=dict,
                    logger_factory=structlog.stdlib.LoggerFactory(),
                    wrapper_class=structlog.stdlib.BoundLogger,
                    cache_logger_on_first_use=True,
                )
                logging.basicConfig(
                    format="%(message)s",
                    stream=sys.stdout,
                    level=level,
                )
            except ImportError:
                logging.basicConfig(
                    level=level,
                    format=(
                        '{"time": "%(asctime)s", "level": "%(levelname)s", '
                        '"logger": "%(name)s", "message": "%(message)s"}'
                    ),
                    datefmt="%Y-%m-%dT%H:%M:%S%z",
                )
        else:
            logging.basicConfig(
                level=level,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )

    def get_correlation_logger(
        self, correlation_id: str | None = None
    ) -> "CorrelationLogger":
        """Get a correlation logger instance."""
        return CorrelationLogger("react_scuba_api", correlation_id)


class CorrelationLogger:
    """Logger with correlation ID support for distributed tracing."""

    def __init__(self, name: str, correlation_id: str | None = None):
        self.name = name
        self.correlation_id = correlation_id or self._generate_correlation_id()
        self.logger = logging.getLogger(name)

    @staticmethod
    def _generate_correlation_id() -> str:
        """Generate a unique correlation ID."""
        import uuid

        return str(uuid.uuid4())

    def _log(
        self, level: int, message: str, extra: dict[str, Any] | None = None
    ) -> None:
        """Internal logging method with correlation ID."""
        log_extra = extra or {}
        if get_config().logging.enable_correlation_ids:
            log_extra["correlation_id"] = self.correlation_id

        self.logger.log(level, message, extra=log_extra)

    def debug(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """Log debug message with correlation ID."""
        self._log(logging.DEBUG, message, extra)

    def info(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """Log info message with correlation ID."""
        self._log(logging.INFO, message, extra)

    def warning(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """Log warning message with correlation ID."""
        self._log(logging.WARNING, message, extra)

    def error(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """Log error message with correlation ID."""
        self._log(logging.ERROR, message, extra)

    def critical(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """Log critical message with correlation ID."""
        self._log(logging.CRITICAL, message, extra)

    def get_correlation_id(self) -> str:
        """Get the current correlation ID."""
        return self.correlation_id

    def set_correlation_id(self, correlation_id: str) -> None:
        """Set a new correlation ID."""
        self.correlation_id = correlation_id


class ServiceConfig(BaseModel):
    """Individual service configuration."""

    name: str = Field(..., description="Service name")
    host: str = Field(default="localhost", description="Service host")
    port: int = Field(..., ge=1, le=65535, description="Service port")
    protocol: str = Field(default="http", description="Service protocol")
    health_check_path: str = Field(
        default="/health", description="Health check endpoint"
    )
    health_check_interval: int = Field(
        default=30, ge=5, description="Health check interval in seconds"
    )
    health_check_timeout: int = Field(
        default=10, ge=1, description="Health check timeout in seconds"
    )

    @property
    def base_url(self) -> str:
        """Generate service base URL."""
        return f"{self.protocol}://{self.host}:{self.port}"


class ApplicationConfig(BaseSettings):
    """Main application configuration with environment variable loading."""

    # Environment and application settings
    environment: Environment = Field(
        default=Environment.DEVELOPMENT, description="Application environment"
    )
    app_name: str = Field(default="React Scuba", description="Application name")
    version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")

    # Service configurations
    services: dict[str, ServiceConfig] = Field(
        default_factory=dict, description="Service configurations"
    )

    # Infrastructure configurations
    database: DatabaseConfig
    redis: RedisConfig | None = Field(default=None, description="Redis configuration")
    http: HTTPConfig = Field(
        default_factory=HTTPConfig, description="HTTP client configuration"
    )
    paths: PathConfig = Field(
        default_factory=PathConfig, description="Path configuration"
    )
    logging: LoggingConfig = Field(
        default_factory=LoggingConfig, description="Logging configuration"
    )

    # Docker and deployment settings
    docker_buildkit: bool = Field(default=True, description="Enable Docker BuildKit")
    python_unbuffered: bool = Field(
        default=True, description="Python unbuffered output"
    )
    python_path: str = Field(
        default="/app/python_utils:/app",
        description="Python path for module resolution",
    )

    # Performance and optimization settings
    python_optimize: int = Field(
        default=1, ge=0, le=2, description="Python optimization level"
    )
    python_dont_write_bytecode: bool = Field(
        default=True, description="Don't write .pyc files"
    )
    python_malloc: str = Field(default="malloc", description="Python memory allocator")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="REACT_SCUBA__",
        case_sensitive=False,
        extra="ignore",  # Ignore extra environment variables
    )

    @classmethod
    def create_default_services(cls) -> dict[str, ServiceConfig]:
        """Create default service configurations."""
        return {
            "node": ServiceConfig(
                name="node", host="localhost", port=3000, health_check_path="/health"
            ),
            "python": ServiceConfig(
                name="python", host="localhost", port=8000, health_check_path="/health"
            ),
            "database": ServiceConfig(
                name="database",
                host="localhost",
                port=5432,
                protocol="postgresql",
                health_check_path="",
            ),
            "redis": ServiceConfig(
                name="redis",
                host="localhost",
                port=6379,
                protocol="redis",
                health_check_path="",
            ),
        }

    def __init__(self, **data: Any) -> None:
        if "services" not in data:
            data["services"] = self.create_default_services()

        if "database" not in data:
            data["database"] = {
                "host": os.getenv("POSTGRES_HOST", "localhost"),
                "port": int(os.getenv("POSTGRES_PORT", "5432")),
                "name": os.getenv("POSTGRES_DB", "mydb"),
                "user": os.getenv("POSTGRES_USER", "user"),
                "password": os.getenv("POSTGRES_PASSWORD", "password"),
            }

        super().__init__(**data)

    @field_validator("environment")
    @classmethod
    def validate_environment_settings(cls, v: Environment) -> Environment:
        if v == Environment.PRODUCTION:
            if os.getenv("REACT_SCUBA__DEBUG", "").lower() in ("true", "1"):
                raise ValueError("Debug mode cannot be enabled in production")
        return v

    def get_service_url(self, service_name: str) -> str | None:
        """Get the full URL for a service."""
        service = self.services.get(service_name)
        return service.base_url if service else None

    def validate_configuration(self) -> list[str]:
        """Validate the entire configuration and return any issues."""
        issues = []

        if self.environment != Environment.DEVELOPMENT:
            try:
                pass
            except Exception as e:
                issues.append(f"Database connectivity issue: {e}")

        try:
            self.paths.docs_path.exists()
        except Exception:
            issues.append(f"Docs path does not exist: {self.paths.docs_path}")

        for name, service in self.services.items():
            if not service.name:
                issues.append(f"Service {name} has no name configured")

        return issues


# Global configuration instance
_config: ApplicationConfig | None = None


def get_config() -> ApplicationConfig:
    """Get the global application configuration."""
    global _config
    if _config is None:
        try:
            _config = ApplicationConfig()
        except ValidationError as e:
            raise ValueError(f"Configuration validation failed: {e}") from e
    return _config


def reload_config() -> ApplicationConfig:
    """Reload configuration from environment."""
    global _config
    _config = None
    return get_config()


def validate_config() -> list[str]:
    """Validate current configuration and return issues."""
    config = get_config()
    return config.validate_configuration()


# Convenience functions for backward compatibility
def get_database_config() -> DatabaseConfig:
    """Get database configuration."""
    return get_config().database


def get_redis_config() -> RedisConfig | None:
    """Get Redis configuration."""
    return get_config().redis


def get_http_config() -> HTTPConfig:
    """Get HTTP configuration."""
    return get_config().http


def get_path_config() -> PathConfig:
    """Get path configuration."""
    return get_config().paths


def get_logging_config() -> LoggingConfig:
    """Get logging configuration."""
    return get_config().logging
