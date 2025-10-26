"""Type aliases specific to MCP modules."""

from typing import Any, TypeAlias

ServerName: TypeAlias = str
ServerConfig: TypeAlias = dict[str, Any]

__all__: list[str] = ["ServerName", "ServerConfig"]
