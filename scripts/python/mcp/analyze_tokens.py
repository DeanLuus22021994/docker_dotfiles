#!/usr/bin/env python3
"""Token Usage Analyzer for MCP Configurations.

Estimates token usage based on tool counts and server configurations
using Python 3.14 type system features.

Examples:
    >>> analyzer = TokenAnalyzer(Path("mcp.json"))
    >>> stats = analyzer.analyze()
    >>> print(stats["estimated_tokens"])
"""

# pylint: disable=logging-fstring-interpolation  # CLI display output

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, TypeAlias

from python.utils.colors import Colors
from python.utils.logging_utils import setup_logger

logger = setup_logger("token_analyzer")

# Type aliases
ServerName: TypeAlias = str
ConfigPath: TypeAlias = Path
TokenCount: TypeAlias = int
ToolCount: TypeAlias = int
ServerConfig: TypeAlias = dict[str, Any]


@dataclass(frozen=True, slots=True)
class TokenStats:
    """Token usage statistics."""

    server_count: int
    tool_count: int
    tokens_per_tool: int
    tokens_per_server: int
    tool_tokens: int
    server_overhead: int
    estimated_tokens: int
    token_range: str
    token_range_k: str
    servers: tuple[ServerName, ...]


class TokenAnalyzer:
    """Analyzes token usage for MCP configurations."""

    # Token estimates per tool (average from schema analysis)
    TOKENS_PER_TOOL: Final[int] = 180  # Average: name, description, input schema

    # Base overhead tokens per server
    TOKENS_PER_SERVER: Final[int] = 50  # Server metadata, connection info

    # Tool count estimates per server (from discovery)
    KNOWN_TOOL_COUNTS: Final[dict[ServerName, ToolCount]] = {
        "playwright": 32,
        "github": 26,
        "filesystem": 14,
        "git": 12,
        "memory": 9,
        "puppeteer": 7,
        "sqlite": 5,
        "postgres": 1,
        "fetch": 1,
    }

    def __init__(self, config_path: ConfigPath) -> None:
        """Initialize analyzer with config file path."""
        self.config_path: ConfigPath = config_path
        self._config: ServerConfig | None = None

    def load_config(self) -> bool:
        """Load MCP configuration from file.

        Returns:
            True if config loaded successfully, False otherwise
        """
        try:
            with open(self.config_path, encoding="utf-8") as f:
                self._config = json.load(f)
            return True
        except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
            logger.error("Failed to load config: %s", e)
            return False

    def analyze(self) -> dict[str, Any]:
        """
        Analyze token usage.

        Returns:
            Dictionary with token usage statistics
        """
        if not self._config:
            return {}

        servers = self._config.get("servers", {})
        metadata = self._config.get("_metadata", {})

        # Get tool count from metadata or calculate
        if "tool_count" in metadata:
            total_tools = metadata["tool_count"]
        else:
            total_tools = self._estimate_tool_count(servers)

        # Calculate token estimates
        server_count = len(servers)
        tool_tokens = total_tools * self.TOKENS_PER_TOOL
        server_overhead = server_count * self.TOKENS_PER_SERVER
        estimated_total = tool_tokens + server_overhead

        # Token range (±15% variance)
        token_min = int(estimated_total * 0.85)
        token_max = int(estimated_total * 1.15)

        return {
            "server_count": server_count,
            "tool_count": total_tools,
            "tokens_per_tool": self.TOKENS_PER_TOOL,
            "tokens_per_server": self.TOKENS_PER_SERVER,
            "tool_tokens": tool_tokens,
            "server_overhead": server_overhead,
            "estimated_tokens": estimated_total,
            "token_range": f"{token_min:,}-{token_max:,}",
            "token_range_k": f"{token_min//1000}-{token_max//1000}k",
            "servers": list(servers.keys()),
        }

    def _estimate_tool_count(self, servers: dict[str, Any]) -> int:
        """Estimate total tool count from server list."""
        total = 0
        for server_name in servers:
            total += self.KNOWN_TOOL_COUNTS.get(server_name, 10)  # Default: 10 tools
        return total

    def compare_profiles(self, other_config_path: Path) -> dict[str, Any]:
        """
        Compare token usage with another configuration.

        Args:
            other_config_path: Path to another mcp config file

        Returns:
            Dictionary with comparison statistics
        """
        other_analyzer = TokenAnalyzer(other_config_path)
        if not other_analyzer.load_config():
            return {}

        current_stats = self.analyze()
        other_stats = other_analyzer.analyze()

        token_diff = other_stats["estimated_tokens"] - current_stats["estimated_tokens"]
        token_diff_percent = (
            (token_diff / current_stats["estimated_tokens"]) * 100
            if current_stats["estimated_tokens"] > 0
            else 0
        )

        tool_diff = other_stats["tool_count"] - current_stats["tool_count"]

        return {
            "current": current_stats,
            "other": other_stats,
            "token_difference": token_diff,
            "token_difference_percent": round(token_diff_percent, 1),
            "tool_difference": tool_diff,
        }


def analyze_token_usage(config_path: Path | str) -> dict[str, Any]:
    """
    Analyze token usage for MCP configuration.

    Args:
        config_path: Path to mcp.json file

    Returns:
        Dictionary with token usage statistics
    """
    if isinstance(config_path, str):
        config_path = Path(config_path)

    analyzer = TokenAnalyzer(config_path)
    if not analyzer.load_config():
        return {}

    return analyzer.analyze()


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Analyze MCP configuration token usage")
    parser.add_argument(
        "config",
        type=Path,
        nargs="?",
        default=Path.cwd() / ".vscode" / "mcp.json",
        help="Path to mcp.json file (or profile in .vscode/profiles/)",
    )
    parser.add_argument(
        "--compare",
        type=Path,
        help="Compare with another configuration",
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    analyzer = TokenAnalyzer(args.config)
    if not analyzer.load_config():
        sys.exit(1)

    if args.compare:
        results = analyzer.compare_profiles(args.compare)
        if not results:
            sys.exit(1)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            current = results["current"]
            other = results["other"]

            logger.info(f"\n{Colors.BOLD}TOKEN USAGE COMPARISON{Colors.RESET}")
            logger.info("=" * 70)

            logger.info(f"\n{Colors.CYAN}Configuration 1:{Colors.RESET} {args.config.name}")
            logger.info(f"  Servers: {current['server_count']}")
            logger.info(f"  Tools: {current['tool_count']}")
            logger.info(
                f"  Estimated Tokens: {current['estimated_tokens']:,} ({current['token_range_k']})"
            )

            logger.info(f"\n{Colors.CYAN}Configuration 2:{Colors.RESET} {args.compare.name}")
            logger.info(f"  Servers: {other['server_count']}")
            logger.info(f"  Tools: {other['tool_count']}")
            logger.info(
                f"  Estimated Tokens: {other['estimated_tokens']:,} ({other['token_range_k']})"
            )

            logger.info(f"\n{Colors.YELLOW}Difference:{Colors.RESET}")
            diff_sign = "+" if results["token_difference"] > 0 else ""
            logger.info(f"  Tools: {diff_sign}{results['tool_difference']}")
            logger.info(
                f"  Tokens: {diff_sign}{results['token_difference']:,} "
                f"({diff_sign}{results['token_difference_percent']}%)"
            )
            logger.info("%s\n", "=" * 70)
    else:
        stats = analyzer.analyze()
        if not stats:
            sys.exit(1)

        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            logger.info(f"\n{Colors.BOLD}TOKEN USAGE ANALYSIS{Colors.RESET}")
            logger.info("=" * 70)
            logger.info(f"\nConfiguration: {args.config.name}")
            logger.info(f"Servers: {stats['server_count']}")
            logger.info(f"Tools: {stats['tool_count']}")
            logger.info(f"\n{Colors.CYAN}Token Breakdown:{Colors.RESET}")
            logger.info(f"  Tool definitions: {stats['tool_tokens']:,} tokens")
            logger.info(f"  Server overhead: {stats['server_overhead']:,} tokens")
            total_msg = f"  {Colors.BOLD}Estimated Total: "
            total_msg += f"{stats['estimated_tokens']:,} tokens{Colors.RESET}"
            logger.info(total_msg)
            logger.info(f"  Range: {stats['token_range']} tokens")
            logger.info(f"  Compact: {stats['token_range_k']}")
            logger.info(f"\n{Colors.GREEN}Servers Enabled:{Colors.RESET}")
            for server in stats["servers"]:
                tool_count = analyzer.KNOWN_TOOL_COUNTS.get(server, "?")
                logger.info(f"  • {server} ({tool_count} tools)")
            logger.info("%s\n", "=" * 70)


if __name__ == "__main__":
    main()
