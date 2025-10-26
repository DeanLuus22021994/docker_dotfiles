"""Constants package for Python scripts.

Constants are grouped by domain/functionality for easy discovery.
All constants use Final type annotation for immutability.
"""

from .formatting import (
    BLACK_LINE_LENGTH,
    DEFAULT_JSON_INDENT,
    MASK_LENGTH,
    MASK_SUFFIX,
    RUFF_LINE_LENGTH,
    SHORT_MASK,
    YAML_LINE_LENGTH,
)
from .logging import DEFAULT_LOG_FORMAT
from .mcp import (
    MCP_PROTOCOL_VERSION,
    MCP_REQUIRED_FIELDS,
    MCP_VALID_COMMANDS,
    TOKENS_PER_SERVER,
    TOKENS_PER_TOOL,
)
from .packages import REQUIRED_PACKAGES
from .paths import (
    DEFAULT_ENCODING,
    DEFAULT_PYTHON_DIRS,
    MARIADB_CONFIG,
    NGINX_CONFIGS,
    POSTGRESQL_CONFIG,
    PYPROJECT_PATH,
)

__all__: list[str] = [
    # Formatting
    "BLACK_LINE_LENGTH",
    "RUFF_LINE_LENGTH",
    "YAML_LINE_LENGTH",
    "DEFAULT_JSON_INDENT",
    "MASK_LENGTH",
    "MASK_SUFFIX",
    "SHORT_MASK",
    # Paths
    "DEFAULT_PYTHON_DIRS",
    "NGINX_CONFIGS",
    "POSTGRESQL_CONFIG",
    "MARIADB_CONFIG",
    "PYPROJECT_PATH",
    "DEFAULT_ENCODING",
    # Packages
    "REQUIRED_PACKAGES",
    # MCP
    "MCP_PROTOCOL_VERSION",
    "MCP_VALID_COMMANDS",
    "MCP_REQUIRED_FIELDS",
    "TOKENS_PER_TOOL",
    "TOKENS_PER_SERVER",
    # Logging
    "DEFAULT_LOG_FORMAT",
]
