"""MCP valid command types enumeration."""

from enum import StrEnum


class MCPCommand(StrEnum):
    """Valid commands for MCP server configuration."""

    NPX = "npx"
    UVX = "uvx"
    NODE = "node"
    PYTHON = "python"
    PYTHON3 = "python3"


__all__: list[str] = ["MCPCommand"]
