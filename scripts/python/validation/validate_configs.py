#!/usr/bin/env python3
"""
Configuration Validation Script

Validates YAML, JSON, nginx, PostgreSQL, and MariaDB configuration files
using modular validator classes. Each config type has a dedicated validator
following the Single Responsibility Principle.

This module uses Python 3.14 type system features including dataclasses,
TypeAlias, Protocol, Literal, and Final for improved type safety.

Exit code: 0=success, 1=failure

Examples:
    >>> from validation.validate_configs import ConfigurationAuditor
    >>> auditor = ConfigurationAuditor()
    >>> report = auditor.validate_all()
    >>> print(report.is_valid)  # True if all configs valid
"""

import json
import subprocess
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from python.types.aliases import ErrorMessage, ExitCode
from python.types.aliases_validation import ConfigType
from python.types.constants import (
    MARIADB_CONFIG,
    NGINX_CONFIGS,
    POSTGRESQL_CONFIG,
    YAML_LINE_LENGTH,
)
from python.utils.colors import error, header, separator, success


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Result of a configuration validation check.

    Attributes:
        passed: Whether validation succeeded
        config_type: Type of configuration validated
        validated_files: Files that were validated
        errors: Error messages from validation
    """

    passed: bool
    config_type: ConfigType
    validated_files: tuple[Path, ...] = field(default_factory=tuple)
    errors: tuple[ErrorMessage, ...] = field(default_factory=tuple)

    @property
    def file_count(self) -> int:
        """Number of files validated."""
        return len(self.validated_files)

    @property
    def error_count(self) -> int:
        """Number of errors found."""
        return len(self.errors)

    @property
    def has_errors(self) -> bool:
        """Check if validation found any errors."""
        return len(self.errors) > 0


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Aggregated results from all configuration validations.

    Attributes:
        results: Tuple of all validation results
    """

    results: tuple[ValidationResult, ...]

    @property
    def is_valid(self) -> bool:
        """Check if all validations passed."""
        return all(result.passed for result in self.results)

    @property
    def total_files(self) -> int:
        """Total number of files validated."""
        return sum(result.file_count for result in self.results)

    @property
    def total_errors(self) -> int:
        """Total number of errors found."""
        return sum(result.error_count for result in self.results)

    @property
    def all_errors(self) -> tuple[ErrorMessage, ...]:
        """Collect all errors from all validations."""
        errors: list[ErrorMessage] = []
        for result in self.results:
            errors.extend(result.errors)
        return tuple(errors)

    @property
    def failed_validators(self) -> tuple[ConfigType, ...]:
        """Get types of validators that failed."""
        return tuple(result.config_type for result in self.results if not result.passed)


class ConfigValidatorProtocol(Protocol):
    """Protocol defining interface for configuration validators."""

    @property
    def config_type(self) -> ConfigType:
        """Type of configuration this validator handles."""
        raise NotImplementedError

    def validate(self) -> ValidationResult:
        """Validate configuration files.

        Returns:
            ValidationResult with pass/fail status and errors
        """
        raise NotImplementedError


class BaseConfigValidator(ABC):
    """Abstract base class for configuration validators.

    Provides common functionality for file discovery and validation.
    """

    def __init__(self, *, verbose: bool = True) -> None:
        """Initialize validator.

        Args:
            verbose: Enable verbose output (default: True)
        """
        self.verbose = verbose

    @property
    @abstractmethod
    def config_type(self) -> ConfigType:
        """Type of configuration this validator handles."""
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> ValidationResult:
        """Validate configuration files."""
        raise NotImplementedError

    def _should_exclude_path(self, path: Path) -> bool:
        """Check if path should be excluded from validation.

        Args:
            path: Path to check

        Returns:
            True if path should be excluded
        """
        excluded_dirs = {".git", "node_modules", ".vscode"}
        return any(excluded in path.parts for excluded in excluded_dirs)

    def _create_error_result(self, error_msg: ErrorMessage) -> ValidationResult:
        """Create ValidationResult for error consistently.

        Args:
            error_msg: Error message

        Returns:
            ValidationResult with passed=False and error
        """
        if self.verbose:
            print(error(error_msg))
        return ValidationResult(
            passed=False,
            config_type=self.config_type,
            errors=(error_msg,),
        )


class YamlValidator(BaseConfigValidator):
    """Validates YAML configuration files using yamllint."""

    @property
    def config_type(self) -> ConfigType:
        return "yaml"

    def validate(self) -> ValidationResult:
        """Validate all YAML files in repository."""
        if self.verbose:
            print(f"\n{header('=== Validating YAML Files ===')}")

        # Find all YAML files
        yaml_files = list(Path(".").rglob("*.yml")) + list(Path(".").rglob("*.yaml"))
        yaml_files = [f for f in yaml_files if not self._should_exclude_path(f)]

        if not yaml_files:
            if self.verbose:
                print("No YAML files found")
            return ValidationResult(passed=True, config_type=self.config_type)

        try:
            # Construct yamllint config string
            config = (
                f"{{extends: default, rules: {{line-length: {{max: {YAML_LINE_LENGTH}}}, "
                "document-start: disable}}}}"
            )
            result = subprocess.run(
                [
                    "yamllint",
                    "-d",
                    config,
                    ".",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                errors = (f"yamllint failed:\n{result.stdout}",)
                if self.verbose:
                    print(error("YAML validation failed"))
                    print(result.stdout)
                return ValidationResult(
                    passed=False,
                    config_type=self.config_type,
                    validated_files=tuple(yaml_files),
                    errors=errors,
                )

            if self.verbose:
                print(success(f"All {len(yaml_files)} YAML files valid"))
            return ValidationResult(
                passed=True,
                config_type=self.config_type,
                validated_files=tuple(yaml_files),
            )

        except FileNotFoundError:
            error_msg = "yamllint not found. Install with: pip install yamllint"
            return self._create_error_result(error_msg)


class JsonValidator(BaseConfigValidator):
    """Validates JSON configuration files using built-in json module."""

    @property
    def config_type(self) -> ConfigType:
        return "json"

    def validate(self) -> ValidationResult:
        """Validate all JSON files in repository."""
        if self.verbose:
            print(f"\n{header('=== Validating JSON Files ===')}")

        # Find all JSON files
        json_files = list(Path(".").rglob("*.json"))
        json_files = [f for f in json_files if not self._should_exclude_path(f)]

        if not json_files:
            if self.verbose:
                print("No JSON files found")
            return ValidationResult(passed=True, config_type=self.config_type)

        errors: list[ErrorMessage] = []
        valid_count = 0

        for json_file in json_files:
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    json.load(f)
                valid_count += 1
            except json.JSONDecodeError as e:
                error_msg = f"{json_file}: {e}"
                errors.append(error_msg)
                if self.verbose:
                    print(error(error_msg))

        if errors:
            if self.verbose:
                print(error(f"{len(errors)} JSON file(s) invalid"))
            return ValidationResult(
                passed=False,
                config_type=self.config_type,
                validated_files=tuple(json_files),
                errors=tuple(errors),
            )

        if self.verbose:
            print(success(f"All {valid_count} JSON files valid"))
        return ValidationResult(
            passed=True,
            config_type=self.config_type,
            validated_files=tuple(json_files),
        )


class NginxValidator(BaseConfigValidator):
    """Validates nginx configuration files using Docker nginx container."""

    @property
    def config_type(self) -> ConfigType:
        return "nginx"

    def validate(self) -> ValidationResult:
        """Validate nginx configuration files."""
        if self.verbose:
            print(f"\n{header('=== Validating nginx Configs ===')}")

        # Find existing nginx configs
        existing_configs = [Path(f) for f in NGINX_CONFIGS if Path(f).exists()]

        if not existing_configs:
            if self.verbose:
                print("No nginx configs found")
            return ValidationResult(passed=True, config_type=self.config_type)

        errors: list[ErrorMessage] = []

        for config in existing_configs:
            try:
                result = subprocess.run(
                    [
                        "docker",
                        "run",
                        "--rm",
                        "-v",
                        f"{config.absolute()}:/etc/nginx/test.conf:ro",
                        "nginx:alpine",
                        "nginx",
                        "-t",
                        "-c",
                        "/etc/nginx/test.conf",
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.returncode != 0:
                    error_msg = f"{config}: nginx validation failed\n{result.stderr}"
                    errors.append(error_msg)
                    if self.verbose:
                        print(error(f"{config}: validation failed"))
                        print(result.stderr)
                else:
                    if self.verbose:
                        print(success(f"{config}: valid"))

            except FileNotFoundError:
                error_msg = "Docker not found. Cannot validate nginx configs without Docker"
                return self._create_error_result(error_msg)

        if errors:
            if self.verbose:
                print(error(f"{len(errors)} nginx config(s) invalid"))
            return ValidationResult(
                passed=False,
                config_type=self.config_type,
                validated_files=tuple(existing_configs),
                errors=tuple(errors),
            )

        if self.verbose:
            print(success(f"All {len(existing_configs)} nginx configs valid"))
        return ValidationResult(
            passed=True,
            config_type=self.config_type,
            validated_files=tuple(existing_configs),
        )


class PostgresqlValidator(BaseConfigValidator):
    """Validates PostgreSQL configuration file with basic syntax checking."""

    @property
    def config_type(self) -> ConfigType:
        return "postgresql"

    def validate(self) -> ValidationResult:
        """Validate PostgreSQL configuration file."""
        if self.verbose:
            print(f"\n{header('=== Validating PostgreSQL Config ===')}")

        if not POSTGRESQL_CONFIG.exists():
            if self.verbose:
                print("PostgreSQL config not found")
            return ValidationResult(passed=True, config_type=self.config_type)

        errors: list[ErrorMessage] = []

        try:
            with open(POSTGRESQL_CONFIG, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    error_msg = f"{POSTGRESQL_CONFIG}:{i}: Missing '=' in configuration line"
                    errors.append(error_msg)
                    if self.verbose:
                        print(error(f"{POSTGRESQL_CONFIG}:{i}: Missing '='"))

            if errors:
                if self.verbose:
                    print(error(f"PostgreSQL config has {len(errors)} error(s)"))
                return ValidationResult(
                    passed=False,
                    config_type=self.config_type,
                    validated_files=(POSTGRESQL_CONFIG,),
                    errors=tuple(errors),
                )

            if self.verbose:
                print(success("PostgreSQL config valid (basic syntax check)"))
            return ValidationResult(
                passed=True,
                config_type=self.config_type,
                validated_files=(POSTGRESQL_CONFIG,),
            )

        except (OSError, IOError, PermissionError) as e:
            error_msg = f"{POSTGRESQL_CONFIG}: {e}"
            return self._create_error_result(error_msg)


class MariadbValidator(BaseConfigValidator):
    """Validates MariaDB configuration file with basic syntax checking."""

    @property
    def config_type(self) -> ConfigType:
        return "mariadb"

    def validate(self) -> ValidationResult:
        """Validate MariaDB configuration file."""
        if self.verbose:
            print(f"\n{header('=== Validating MariaDB Config ===')}")

        if not MARIADB_CONFIG.exists():
            if self.verbose:
                print("MariaDB config not found")
            return ValidationResult(passed=True, config_type=self.config_type)

        errors: list[ErrorMessage] = []

        try:
            with open(MARIADB_CONFIG, "r", encoding="utf-8") as f:
                lines = f.readlines()

            in_section = False
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("[") and line.endswith("]"):
                    in_section = True
                    continue

                if in_section and "=" not in line and "-" not in line:
                    error_msg = f"{MARIADB_CONFIG}:{i}: Invalid configuration line"
                    errors.append(error_msg)
                    if self.verbose:
                        print(error(f"{MARIADB_CONFIG}:{i}: Invalid line"))

            if errors:
                if self.verbose:
                    print(error(f"MariaDB config has {len(errors)} error(s)"))
                return ValidationResult(
                    passed=False,
                    config_type=self.config_type,
                    validated_files=(MARIADB_CONFIG,),
                    errors=tuple(errors),
                )

            if self.verbose:
                print(success("MariaDB config valid (basic syntax check)"))
            return ValidationResult(
                passed=True,
                config_type=self.config_type,
                validated_files=(MARIADB_CONFIG,),
            )

        except (OSError, IOError, PermissionError) as e:
            error_msg = f"{MARIADB_CONFIG}: {e}"
            return self._create_error_result(error_msg)


class ConfigurationAuditor:
    """Orchestrates configuration validation across multiple validators.

    Runs YAML, JSON, nginx, PostgreSQL, and MariaDB validators,
    aggregating results into a comprehensive report.

    Example:
        >>> auditor = ConfigurationAuditor()
        >>> report = auditor.validate_all()
        >>> if report.is_valid:
        ...     print("All configs valid!")
    """

    def __init__(self, *, verbose: bool = True) -> None:
        """Initialize auditor with validators.

        Args:
            verbose: Enable verbose output (default: True)
        """
        self.verbose = verbose
        self.validators: tuple[BaseConfigValidator, ...] = (
            YamlValidator(verbose=verbose),
            JsonValidator(verbose=verbose),
            NginxValidator(verbose=verbose),
            PostgresqlValidator(verbose=verbose),
            MariadbValidator(verbose=verbose),
        )

    def validate_all(self) -> ValidationReport:
        """Run all configuration validators.

        Returns:
            ValidationReport with aggregated results
        """
        if self.verbose:
            print(separator())
            print(header("Configuration Validation"))
            print(separator())

        results: list[ValidationResult] = []
        for validator in self.validators:
            result = validator.validate()
            results.append(result)

        return ValidationReport(results=tuple(results))

    def print_summary(self, report: ValidationReport) -> None:
        """Print human-readable summary of validation results.

        Args:
            report: Report to summarize
        """
        print(f"\n{separator()}")
        if report.is_valid:
            print(success("ALL VALIDATIONS PASSED"))
        else:
            print(error(f"VALIDATION FAILED ({report.total_errors} error(s))"))

        print(separator())

        if not report.is_valid and report.all_errors:
            print("\\nErrors:")
            for err in report.all_errors:
                print(f"  - {err}")


def validate_yaml_files() -> ValidationResult:
    """Validate YAML configuration files (simplified interface).
    
    Returns:
        Validation result
    """
    validator = YamlValidator()
    return validator.validate()


def validate_json_files() -> ValidationResult:
    """Validate JSON configuration files (simplified interface).
    
    Returns:
        Validation result
    """
    validator = JsonValidator()
    return validator.validate()


def validate_nginx_configs() -> ValidationResult:
    """Validate nginx configuration files (simplified interface).
    
    Returns:
        Validation result
    """
    validator = NginxValidator()
    return validator.validate()


def validate_postgresql_config() -> ValidationResult:
    """Validate PostgreSQL configuration file (simplified interface).
    
    Returns:
        Validation result
    """
    validator = PostgresqlValidator()
    return validator.validate()


def validate_mariadb_config() -> ValidationResult:
    """Validate MariaDB configuration file (simplified interface).
    
    Returns:
        Validation result
    """
    validator = MariadbValidator()
    return validator.validate()


__all__ = [
    "ValidationResult",
    "ValidationReport",
    "BaseConfigValidator",
    "YamlValidator",
    "JsonValidator",
    "NginxValidator",
    "PostgresqlValidator",
    "MariadbValidator",
    "ConfigurationAuditor",
    "validate_yaml_files",
    "validate_json_files",
    "validate_nginx_configs",
    "validate_postgresql_config",
    "validate_mariadb_config",
]


def main() -> ExitCode:
    """Run all configuration validations and return exit code.

    Returns:
        0 if all validations passed, 1 otherwise
    """
    auditor = ConfigurationAuditor()
    report = auditor.validate_all()
    auditor.print_summary(report)

    return 0 if report.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
