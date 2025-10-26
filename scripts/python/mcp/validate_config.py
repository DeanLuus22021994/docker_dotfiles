#!/usr/bin/env python3
"""MCP Configuration Validator.

Validates MCP server configurations against JSON schema and
protocol requirements using Python 3.14 type system features.

Examples:
    >>> validator = MCPConfigValidator(Path("mcp.json"))
    >>> success, errors, warnings = validator.validate()
    >>> print(f"Valid: {success}")
"""

# pylint: disable=logging-fstring-interpolation  # CLI display output

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final, TypeAlias

# Add parent directories to path for imports
_SCRIPTS_DIR: Final[Path] = Path(__file__).parent.parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from python.utils.colors import Colors
from python.utils.logging_utils import setup_logger

logger = setup_logger("mcp_validator")

# Type aliases
ServerName: TypeAlias = str
FieldName: TypeAlias = str
ErrorMessage: TypeAlias = str
WarningMessage: TypeAlias = str
ServerConfig: TypeAlias = dict[str, Any]


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Result of MCP configuration validation."""

    success: bool
    errors: tuple[ErrorMessage, ...]
    warnings: tuple[WarningMessage, ...]

    @property
    def has_errors(self) -> bool:
        """Check if validation has errors."""
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """Check if validation has warnings."""
        return len(self.warnings) > 0


class MCPConfigValidator:
    """Validates MCP configuration files."""

    # MCP protocol version
    PROTOCOL_VERSION: Final[str] = "2024-11-05"

    # Valid commands
    VALID_COMMANDS: Final[tuple[str, ...]] = ("npx", "uvx", "node", "python", "python3")

    # Required fields
    REQUIRED_SERVER_FIELDS: Final[tuple[FieldName, ...]] = ("command", "args")

    def __init__(self, config_path: Path) -> None:
        """Initialize validator with config file path."""
        self.config_path: Path = config_path
        self._errors: list[ErrorMessage] = []
        self._warnings: list[WarningMessage] = []
        self._config: ServerConfig | None = None

    @property
    def errors(self) -> list[ErrorMessage]:
        """Get validation errors."""
        return self._errors

    @property
    def warnings(self) -> list[WarningMessage]:
        """Get validation warnings."""
        return self._warnings

    @property
    def config(self) -> ServerConfig | None:
        """Get loaded configuration."""
        return self._config

    def validate(self) -> tuple[bool, list[str], list[str]]:
        """
        Validate MCP configuration.

        Returns:
            Tuple of (success, errors, warnings)
        """
        self._errors = []
        self._warnings = []

        # Load and parse JSON
        if not self._load_json():
            return (False, self.errors, self.warnings)

        # Validate structure
        self._validate_structure()

        # Validate servers
        self._validate_servers()

        # Validate metadata (if present)
        self._validate_metadata()

        success = len(self.errors) == 0
        return (success, self.errors, self.warnings)

    def _load_json(self) -> bool:
        """Load and parse JSON configuration."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)
            return True
        except FileNotFoundError:
            self.errors.append(f"Config file not found: {self.config_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False
        except (OSError, PermissionError) as e:
            self.errors.append(f"Failed to load config: {e}")
            return False

    def _validate_structure(self) -> None:
        """Validate top-level structure."""
        if not isinstance(self.config, dict):
            self.errors.append("Config must be a JSON object")
            return

        if "servers" not in self.config:
            self.errors.append("Missing required field: 'servers'")
            return

        if not isinstance(self.config["servers"], dict):
            self.errors.append("Field 'servers' must be an object")
            return

        if len(self.config["servers"]) == 0:
            self.warnings.append("No servers configured")

    def _validate_servers(self) -> None:
        """Validate server configurations."""
        if not self.config or "servers" not in self.config:
            return

        servers = self.config["servers"]

        for server_name, server_config in servers.items():
            self._validate_server(server_name, server_config)

    def _validate_server(self, name: str, config: dict[str, Any]) -> None:
        """Validate a single server configuration."""
        # Check required fields
        for field_name in self.REQUIRED_SERVER_FIELDS:
            if field_name not in config:
                self.errors.append(f"Server '{name}': Missing required field '{field_name}'")

        # Validate command
        if "command" in config:
            command = config["command"]
            if not isinstance(command, str):
                self.errors.append(f"Server '{name}': 'command' must be a string")
            elif command not in self.VALID_COMMANDS:
                self.warnings.append(
                    f"Server '{name}': Unusual command '{command}' "
                    f"(expected: {', '.join(self.VALID_COMMANDS)})"
                )

        # Validate args
        if "args" in config:
            args = config["args"]
            if not isinstance(args, list):
                self.errors.append(f"Server '{name}': 'args' must be an array")
            else:
                for i, arg in enumerate(args):
                    if not isinstance(arg, str):
                        self.errors.append(f"Server '{name}': args[{i}] must be a string")

        # Validate env (optional)
        if "env" in config:
            env = config["env"]
            if not isinstance(env, dict):
                self.errors.append(f"Server '{name}': 'env' must be an object")
            else:
                for key, value in env.items():
                    if not isinstance(value, str):
                        self.errors.append(f"Server '{name}': env['{key}'] must be a string")

    def _validate_metadata(self) -> None:
        """Validate metadata (if present)."""
        if not self.config or "_metadata" not in self.config:
            return

        metadata = self.config["_metadata"]

        if not isinstance(metadata, dict):
            self.errors.append("Field '_metadata' must be an object")
            return

        # Validate metadata fields
        if "profile_name" in metadata and not isinstance(metadata["profile_name"], str):
            self.errors.append("Metadata 'profile_name' must be a string")

        if "tool_count" in metadata and not isinstance(metadata["tool_count"], int):
            self.errors.append("Metadata 'tool_count' must be a number")

        if "servers_enabled" in metadata:
            servers_enabled = metadata["servers_enabled"]
            if not isinstance(servers_enabled, list):
                self.errors.append("Metadata 'servers_enabled' must be an array")
            else:
                # Check if all listed servers exist
                actual_servers = set(self.config.get("servers", {}).keys())
                for server in servers_enabled:
                    if server not in actual_servers:
                        self.warnings.append(
                            f"Metadata lists server '{server}' but it's not configured"
                        )


def validate_mcp_config(config_path: Path | str) -> tuple[bool, list[str], list[str]]:
    """
    Validate MCP configuration file.

    Args:
        config_path: Path to mcp.json file

    Returns:
        Tuple of (success, errors, warnings)
    """
    if isinstance(config_path, str):
        config_path = Path(config_path)

    validator = MCPConfigValidator(config_path)
    return validator.validate()


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Validate MCP configuration")
    parser.add_argument(
        "config",
        type=Path,
        nargs="?",
        default=Path.cwd() / ".vscode" / "mcp.json",
        help="Path to mcp.json file (or profile in .vscode/profiles/)",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")

    args = parser.parse_args()

    logger.info(f"Validating: {args.config}")
    success, errors, warnings = validate_mcp_config(args.config)

    # Print errors
    if errors:
        logger.error(f"{Colors.RED}{Colors.BOLD}ERRORS:{Colors.RESET}")
        for error in errors:
            logger.error(f"  {Colors.RED}✗{Colors.RESET} {error}")

    # Print warnings
    if warnings:
        logger.warning(f"{Colors.YELLOW}{Colors.BOLD}WARNINGS:{Colors.RESET}")
        for warning in warnings:
            logger.warning(f"  {Colors.YELLOW}⚠{Colors.RESET} {warning}")

    # Print summary
    if success and not warnings:
        logger.info(f"{Colors.GREEN}✓ Configuration is valid{Colors.RESET}")
        sys.exit(0)
    elif success and warnings:
        if args.strict:
            logger.error(f"{Colors.RED}✗ Validation failed (strict mode){Colors.RESET}")
            sys.exit(1)
        else:
            logger.info(f"{Colors.YELLOW}⚠ Configuration is valid with warnings{Colors.RESET}")
            sys.exit(0)
    else:
        logger.error(f"{Colors.RED}✗ Validation failed{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
