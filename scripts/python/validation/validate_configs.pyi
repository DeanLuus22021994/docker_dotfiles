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
    def file_count(self) -> int: ...
    @property
    def error_count(self) -> int: ...
    @property
    def has_errors(self) -> bool: ...

@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Aggregated results from all configuration validations."""

    results: tuple[ValidationResult, ...]

    @property
    def is_valid(self) -> bool: ...
    @property
    def total_files(self) -> int: ...
    @property
    def total_errors(self) -> int: ...
    @property
    def all_errors(self) -> tuple[ErrorMessage, ...]: ...
    @property
    def failed_validators(self) -> tuple[ConfigType, ...]: ...

class ConfigValidatorProtocol(Protocol):
    """Protocol for configuration validators."""

    @property
    def config_type(self) -> ConfigType: ...
    def validate(self) -> ValidationResult: ...

class BaseConfigValidator(ABC):
    """Abstract base class for configuration validators."""

    verbose: bool

    def __init__(self, *, verbose: bool = True) -> None: ...
    @property
    def config_type(self) -> ConfigType: ...
    def validate(self) -> ValidationResult: ...
    def _should_exclude_path(self, path: Path) -> bool: ...

class YamlValidator(BaseConfigValidator):
    """Validates YAML configuration files."""

    @property
    def config_type(self) -> ConfigType: ...
    def validate(self) -> ValidationResult: ...

class JsonValidator(BaseConfigValidator):
    """Validates JSON configuration files."""

    @property
    def config_type(self) -> ConfigType: ...
    def validate(self) -> ValidationResult: ...

class NginxValidator(BaseConfigValidator):
    """Validates nginx configuration files."""

    @property
    def config_type(self) -> ConfigType: ...
    def validate(self) -> ValidationResult: ...

class PostgresqlValidator(BaseConfigValidator):
    """Validates PostgreSQL configuration file."""

    @property
    def config_type(self) -> ConfigType: ...
    def validate(self) -> ValidationResult: ...

class MariadbValidator(BaseConfigValidator):
    """Validates MariaDB configuration file."""

    @property
    def config_type(self) -> ConfigType: ...
    def validate(self) -> ValidationResult: ...

class ConfigurationAuditor:
    """Orchestrates configuration validation."""

    verbose: bool
    validators: tuple[BaseConfigValidator, ...]

    def __init__(self, *, verbose: bool = True) -> None: ...
    def validate_all(self) -> ValidationReport: ...
    def print_summary(self, report: ValidationReport) -> None: ...

# Backward-compatible function wrappers for testing
def validate_json_files(verbose: bool = True) -> ValidationResult: ...
def validate_yaml_files(verbose: bool = True) -> ValidationResult: ...
def validate_nginx_configs(verbose: bool = True) -> ValidationResult: ...
def validate_postgresql_config(verbose: bool = True) -> ValidationResult: ...
def validate_mariadb_config(verbose: bool = True) -> ValidationResult: ...

def main() -> ExitCode:
    """Run all configuration validations."""
    ...

__all__: list[str]
