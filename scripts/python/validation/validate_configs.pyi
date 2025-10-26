"""Type stubs for validate_configs module.

Provides type hints for configuration validation utilities.
"""

from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal, Protocol, TypeAlias

from ..utils.file_utils import StrPath

# Type aliases
ConfigType: TypeAlias = Literal["yaml", "json", "nginx", "postgresql", "mariadb"]
ErrorMessage: TypeAlias = str
ConfigPath: TypeAlias = StrPath
ExitCode: TypeAlias = int

# Constants
YAML_LINE_LENGTH: Final[int]
NGINX_CONFIGS: Final[tuple[str, ...]]
POSTGRESQL_CONFIG: Final[Path]
MARIADB_CONFIG: Final[Path]

@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Result of a configuration validation check."""

    passed: bool
    config_type: ConfigType
    validated_files: tuple[Path, ...]
    errors: tuple[ErrorMessage, ...]

    @property
    def file_count(self) -> int:
        """Number of files validated."""
    @property
    def error_count(self) -> int:
        """Number of errors found."""
    @property
    def has_errors(self) -> bool:
        """Check if any errors exist."""

@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Aggregated results from all configuration validations."""

    results: tuple[ValidationResult, ...]

    @property
    def is_valid(self) -> bool:
        """Check if all validations passed."""
    @property
    def total_files(self) -> int:
        """Total number of files validated."""
    @property
    def total_errors(self) -> int:
        """Total number of errors found."""
    @property
    def all_errors(self) -> tuple[ErrorMessage, ...]:
        """All error messages combined."""
    @property
    def failed_validators(self) -> tuple[ConfigType, ...]:
        """Config types that failed validation."""

class ConfigValidatorProtocol(Protocol):
    """Protocol for configuration validators."""

    @property
    def config_type(self) -> ConfigType:
        """Type of configuration being validated."""
    def validate(self) -> ValidationResult:
        """Validate configuration files."""

class BaseConfigValidator(ABC):
    """Abstract base class for configuration validators."""

    verbose: bool

    @property
    def config_type(self) -> ConfigType:
        """Type of configuration being validated."""
    def validate(self) -> ValidationResult:
        """Validate configuration files."""
    def _should_exclude_path(self, path: Path, /) -> bool:
        """Check if path should be excluded from validation."""

class YamlValidator(BaseConfigValidator):
    """Validates YAML configuration files."""

    @property
    def config_type(self) -> ConfigType:
        """Type of configuration being validated."""
    def validate(self) -> ValidationResult:
        """Validate YAML configuration files."""

class JsonValidator(BaseConfigValidator):
    """Validates JSON configuration files."""

    @property
    def config_type(self) -> ConfigType:
        """Type of configuration being validated."""
    def validate(self) -> ValidationResult:
        """Validate JSON configuration files."""

class NginxValidator(BaseConfigValidator):
    """Validates nginx configuration files."""

    @property
    def config_type(self) -> ConfigType:
        """Type of configuration being validated."""
    def validate(self) -> ValidationResult:
        """Validate nginx configuration files."""

class PostgresqlValidator(BaseConfigValidator):
    """Validates PostgreSQL configuration file."""

    @property
    def config_type(self) -> ConfigType:
        """Type of configuration being validated."""
    def validate(self) -> ValidationResult:
        """Validate PostgreSQL configuration file."""

class MariadbValidator(BaseConfigValidator):
    """Validates MariaDB configuration file."""

    @property
    def config_type(self) -> ConfigType:
        """Type of configuration being validated."""
    def validate(self) -> ValidationResult:
        """Validate MariaDB configuration file."""

class ConfigurationAuditor:
    """Orchestrates configuration validation."""

    validators: tuple[BaseConfigValidator, ...]

    def validate_all(self) -> ValidationReport:
        """Validate all configured validators."""

def validate_yaml_files() -> ValidationResult:
    """Validate YAML configuration files."""

def validate_json_files() -> ValidationResult:
    """Validate JSON configuration files."""

def validate_nginx_configs() -> ValidationResult:
    """Validate nginx configuration files."""

def validate_postgresql_config() -> ValidationResult:
    """Validate PostgreSQL configuration file."""

def validate_mariadb_config() -> ValidationResult:
    """Validate MariaDB configuration file."""

def main() -> ExitCode:
    """Run all configuration validations."""

__all__: list[str]
