"""Common error handling patterns to eliminate code duplication.

Provides reusable error handlers for common failure scenarios like
missing tools, file not found, etc.

Python 3.14 compatible with strict typing.
"""

from python.types.aliases import ErrorMessage
from python.utils.colors import error as format_error


def handle_tool_not_found(
    tool_name: str,
    *,
    verbose: bool = True,
) -> ErrorMessage:
    """Handle FileNotFoundError for missing tools consistently.

    Args:
        tool_name: Name of the missing tool
        verbose: Whether to print error message

    Returns:
        Error message string

    Example:
        >>> error_msg = handle_tool_not_found("pip", verbose=True)
        >>> return DependencyCheckResult(
        ...     passed=False,
        ...     check_name=self.check_name,
        ...     errors=(error_msg,)
        ... )
    """
    error_msg: ErrorMessage = f"{tool_name} not found"
    if verbose:
        print(format_error(error_msg))

    return error_msg


def handle_file_not_found(
    file_path: str,
    *,
    verbose: bool = True,
) -> ErrorMessage:
    """Handle file not found errors consistently.

    Args:
        file_path: Path to the missing file
        verbose: Whether to print error message

    Returns:
        Error message string
    """
    error_msg: ErrorMessage = f"File not found: {file_path}"
    if verbose:
        print(format_error(error_msg))

    return error_msg


__all__: list[str] = [
    "handle_tool_not_found",
    "handle_file_not_found",
]
