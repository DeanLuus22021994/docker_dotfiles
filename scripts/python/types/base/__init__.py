"""Base classes and protocols for common patterns.

Provides reusable abstractions to eliminate duplicate code across modules.
"""

from .checker import BaseCommandChecker
from .error_handlers import handle_file_not_found, handle_tool_not_found
from .protocols import CheckerProtocol, CommandRunnerProtocol, ValidatorProtocol
from .results import BaseResult

__all__: list[str] = [
    "BaseResult",
    "CheckerProtocol",
    "ValidatorProtocol",
    "CommandRunnerProtocol",
    "BaseCommandChecker",
    "handle_tool_not_found",
    "handle_file_not_found",
]
