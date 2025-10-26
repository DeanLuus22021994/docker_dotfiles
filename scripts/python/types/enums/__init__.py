"""Enumeration types for the Python scripts package.

Each enum type is defined in its own module for clarity and maintainability.
All enums use Python 3.14's StrEnum or IntEnum for type safety.
"""

from .check_status import CheckStatus
from .config_type import ConfigType
from .exit_code import ExitCode
from .log_level import CRITICAL, DEBUG, ERROR, INFO, WARNING, LogLevel
from .mcp_command import MCPCommand
from .tool_name import QualityTool

__all__: list[str] = [
    "LogLevel",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "ConfigType",
    "CheckStatus",
    "ExitCode",
    "MCPCommand",
    "QualityTool",
]
