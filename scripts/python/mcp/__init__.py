"""
MCP (Model Context Protocol) management utilities.

This module provides tools for validating, analyzing, and managing
MCP server configurations for VS Code Copilot integration.
"""

from .validate_config import validate_mcp_config, MCPConfigValidator
from .analyze_tokens import analyze_token_usage, TokenAnalyzer

__all__ = [
    "validate_mcp_config",
    "MCPConfigValidator",
    "analyze_token_usage",
    "TokenAnalyzer",
]

__version__ = "1.0.0"
