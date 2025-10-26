"""Configuration file type enumeration."""

from enum import StrEnum


class ConfigType(StrEnum):
    """Types of configuration files that can be validated."""

    YAML = "yaml"
    JSON = "json"
    NGINX = "nginx"
    POSTGRESQL = "postgresql"
    MARIADB = "mariadb"


__all__: list[str] = ["ConfigType"]
