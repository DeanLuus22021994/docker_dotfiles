"""MCP (Model Context Protocol) constants."""

from typing import Final

# Protocol version
MCP_PROTOCOL_VERSION: Final[str] = "2024-11-05"

# Valid MCP server commands
MCP_VALID_COMMANDS: Final[tuple[str, ...]] = ("npx", "uvx", "node", "python", "python3")

# Required configuration fields
MCP_REQUIRED_FIELDS: Final[tuple[str, ...]] = ("command", "args")

# Token estimation constants
TOKENS_PER_TOOL: Final[int] = 180  # Average: name, description, input schema
TOKENS_PER_SERVER: Final[int] = 50  # Server metadata, connection info

__all__: list[str] = [
    "MCP_PROTOCOL_VERSION",
    "MCP_VALID_COMMANDS",
    "MCP_REQUIRED_FIELDS",
    "TOKENS_PER_TOOL",
    "TOKENS_PER_SERVER",
]
