from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Sequence
from typing import (
    TYPE_CHECKING,
    Any,
    Protocol,
    cast,
)

from ..config.settings import HTTPConfig, PathConfig
from ..models.models import ComponentInventoryConfig, LinkCheckConfig
from ..services.component_inventory import ComponentInventoryService
from ..services.link_checker import LinkCheckerService

"""
MCP (Model Context Protocol) server for React Scuba utilities.

This module implements an MCP server that exposes documentation utilities
as MCP tools for integration with AI assistants and other MCP clients.
"""

_MCPTool: Any = None
_MCPServerImpl: Any = None
_MCPTextContent: Any = None

try:
    import mcp.server.stdio
    from mcp import Tool as _MCPTool_import
    from mcp.server import Server as _MCPServerImpl_import
    from mcp.types import TextContent as _MCPTextContent_import

    _MCPTool = _MCPTool_import
    _MCPServerImpl = _MCPServerImpl_import
    _MCPTextContent = _MCPTextContent_import
    MCP_AVAILABLE = True
except Exception:
    MCP_AVAILABLE = False

if TYPE_CHECKING:
    from mcp import Tool
    from mcp.server import Server
    from mcp.types import TextContent
else:
    Tool = Any
    Server = Any
    TextContent = Any


class _MCPServerLike(Protocol):
    """Protocol describing the minimal MCP server API used here."""

    def __init__(self, name: str) -> None: ...

    def run(
        self,
        read_stream: Any,
        write_stream: Any,
        initialization_options: Any,
        raise_exceptions: bool = False,
        stateless: bool = False,
    ) -> Awaitable[None]: ...

    def create_initialization_options(self) -> Any: ...

    def register_tool(
        self,
        handler: Callable[[str, dict[str, Any]], Awaitable[Sequence[TextContent]]],
    ) -> None:
        """
        Register a tool handler directly when the MCP server exposes register_tool.
        The handler should accept (name, arguments) and return an awaitable sequence
        of TextContent.
        """

    def call_tool(
        self,
        handler: Callable[[str, dict[str, Any]], Awaitable[Sequence[TextContent]]],
    ) -> None:
        """
        Older MCP API may provide call_tool(handler) which registers the
        handler directly (non-decorator form). We type it as accepting the handler.
        """


class ReactScubaMCPServer:
    """
    MCP server for React Scuba documentation utilities.

    Provides tools for link checking and component inventory generation
    through the Model Context Protocol.
    """

    def __init__(self) -> None:
        if not MCP_AVAILABLE or _MCPServerImpl is None:
            raise ImportError("MCP package is required for MCP server functionality")

        self.server: _MCPServerLike = cast(
            _MCPServerLike, _MCPServerImpl("react-scuba-utils")
        )
        self.path_config = PathConfig()
        self.http_config = HTTPConfig()

        self._register_tools()

    def _tool_definitions(self) -> list[Tool]:
        """Return runtime Tool objects describing the tools we expose."""
        assert MCP_AVAILABLE and _MCPTool is not None
        return [
            _MCPTool(
                name="check_documentation_links",
                description="Check all links in documentation files for validity",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "docs_path": {
                            "type": "string",
                            "description": "Path to documentation directory",
                            "default": "docs",
                        },
                        "max_workers": {
                            "type": "integer",
                            "description": "Maximum number of concurrent workers",
                            "default": 10,
                        },
                        "use_interpreters": {
                            "type": "boolean",
                            "description": ("Use concurrent interpreters if available"),
                            "default": True,
                        },
                    },
                },
            ),
            _MCPTool(
                name="generate_component_inventory",
                description=(
                    "Generate an inventory of React components in the source code"
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "src_path": {
                            "type": "string",
                            "description": "Path to source directory",
                            "default": "src",
                        },
                        "extensions": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "File extensions to scan",
                            "default": ["*.jsx", "*.js", "*.tsx", "*.ts"],
                        },
                    },
                },
            ),
            _MCPTool(
                name="get_component_info",
                description="Get detailed information about a specific component",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "component_name": {
                            "type": "string",
                            "description": "Name of the component to analyze",
                        },
                        "src_path": {
                            "type": "string",
                            "description": "Path to source directory",
                            "default": "src",
                        },
                    },
                    "required": ["component_name"],
                },
            ),
        ]

    def _register_tools(self) -> None:
        async def call_tool_handler(
            name: str,
            arguments: dict[str, Any],
        ) -> Sequence[TextContent]:
            if name == "check_documentation_links":
                return await self._check_links_tool(arguments)
            if name == "generate_component_inventory":
                return await self._generate_inventory_tool(arguments)
            if name == "get_component_info":
                return await self._get_component_info_tool(arguments)
            raise ValueError(f"Unknown tool: {name}")

        if hasattr(self.server, "register_tool"):
            for tool in self._tool_definitions():
                try:
                    metadata_register = getattr(
                        self.server, "register_tool_metadata", None
                    )
                    if metadata_register:
                        metadata_register(tool)
                except Exception:
                    pass

            self.server.register_tool(call_tool_handler)
            return

        if hasattr(self.server, "call_tool"):
            self.server.call_tool(call_tool_handler)
            return

        raise RuntimeError("MCP server does not expose a tool registration API")

    async def _check_links_tool(
        self,
        arguments: dict[str, Any],
    ) -> Sequence[TextContent]:
        docs_path = arguments.get("docs_path", "docs")
        max_workers = arguments.get("max_workers", 10)
        use_interpreters = arguments.get("use_interpreters", True)

        self.path_config = PathConfig(docs_path=docs_path)

        config = LinkCheckConfig(
            max_workers=max_workers, use_interpreters=use_interpreters
        )
        service = LinkCheckerService(config, self.path_config, self.http_config)

        results = service.check_links_concurrent()

        output = "Link Check Results:\n"
        output += f"✅ Valid links: {len(results['valid'])}\n"
        output += f"❌ Broken links: {len(results['broken'])}\n"
        output += f"⏭️  Skipped links: {len(results['skipped'])}\n"

        if results["broken"]:
            output += "\n❌ Broken links:\n"
            for link in results["broken"][:10]:
                output += f"  - {link}\n"
            if len(results["broken"]) > 10:
                remaining = len(results["broken"]) - 10
                output += f"  ... and {remaining} more\n"

        assert _MCPTextContent is not None
        return [_MCPTextContent(type="text", text=output)]

    async def _generate_inventory_tool(
        self,
        arguments: dict[str, Any],
    ) -> Sequence[TextContent]:
        src_path = arguments.get("src_path", "src")
        extensions = arguments.get("extensions", ["*.jsx", "*.js", "*.tsx", "*.ts"])

        self.path_config = PathConfig(src_path=src_path)

        config = ComponentInventoryConfig(src_path=src_path, extensions=extensions)
        service = ComponentInventoryService(config, self.path_config)

        inventory = service.generate_inventory()

        output = "Component Inventory:\n"
        output += f"📄 Pages: {len(inventory['pages'])}\n"
        output += f"🧩 Components: {len(inventory['components'])}\n"
        output += f"🪝 Hooks: {len(inventory['hooks'])}\n"
        output += f"🛠️  Utils: {len(inventory['utils'])}\n"

        for category, components in inventory.items():
            if components:
                output += f"\n{category.upper()}:\n"
                for comp in components[:5]:
                    output += f"  - {comp['name']} ({comp['file']})\n"
                if len(components) > 5:
                    remaining = len(components) - 5
                    output += f"  ... and {remaining} more\n"

        assert _MCPTextContent is not None
        return [_MCPTextContent(type="text", text=output)]

    async def _get_component_info_tool(
        self,
        arguments: dict[str, Any],
    ) -> Sequence[TextContent]:
        component_name = arguments["component_name"]
        src_path = arguments.get("src_path", "src")

        self.path_config = PathConfig(src_path=src_path)

        config = ComponentInventoryConfig(src_path=src_path)
        service = ComponentInventoryService(config, self.path_config)

        inventory = service.generate_inventory()

        for category, components in inventory.items():
            for comp in components:
                if comp["name"] == component_name:
                    output = f"Component Information: {component_name}\n"
                    output += f"Category: {category}\n"
                    output += f"File: {comp['file']}\n"
                    output += f"Path: {comp['path']}\n"
                    output += f"Size: {comp['size_bytes']} bytes\n"
                    exports_str = (
                        ", ".join(comp["exports"]) if comp["exports"] else "None"
                    )
                    output += f"Exports: {exports_str}\n"
                    imports_str = (
                        ", ".join(comp["imports"]) if comp["imports"] else "None"
                    )
                    output += f"Imports: {imports_str}\n"
                    assert _MCPTextContent is not None
                    return [_MCPTextContent(type="text", text=output)]

        assert _MCPTextContent is not None
        return [
            _MCPTextContent(type="text", text=f"Component '{component_name}' not found")
        ]

    async def run(self) -> None:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )


def main() -> int:
    """MCP server entry point."""
    if not MCP_AVAILABLE:
        print("❌ MCP package is required. Install with: pip install mcp")
        return 1

    server = ReactScubaMCPServer()
    asyncio.run(server.run())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
