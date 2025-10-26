"""Path constants for file and directory locations."""

from pathlib import Path
from typing import Final

# Python source directories
DEFAULT_PYTHON_DIRS: Final[tuple[str, ...]] = ("scripts/python/", "scripts/orchestrator.py")

# Configuration file paths
NGINX_CONFIGS: Final[tuple[str, ...]] = (
    ".config/nginx/loadbalancer.conf",
    ".config/nginx/main.conf",
    ".config/nginx/default.conf",
)
POSTGRESQL_CONFIG: Final[Path] = Path(".config/database/postgresql.conf")
MARIADB_CONFIG: Final[Path] = Path(".config/database/mariadb.conf")
PYPROJECT_PATH: Final[Path] = Path("pyproject.toml")

# File encoding
DEFAULT_ENCODING: Final[str] = "utf-8"

__all__: list[str] = [
    "DEFAULT_PYTHON_DIRS",
    "NGINX_CONFIGS",
    "POSTGRESQL_CONFIG",
    "MARIADB_CONFIG",
    "PYPROJECT_PATH",
    "DEFAULT_ENCODING",
]
