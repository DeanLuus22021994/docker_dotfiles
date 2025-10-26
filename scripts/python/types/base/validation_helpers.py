"""Validation helper functions to eliminate duplicate patterns.

Provides reusable validation logic for common patterns like checking
environment variables, validating configurations, etc.

Python 3.14 compatible with strict typing.
"""

from typing import Any, Protocol

from python.types.aliases import ErrorMessage
from python.utils.colors import error, success


class VarConfigProtocol(Protocol):
    """Protocol for environment variable configuration objects."""

    @property
    def is_set(self) -> bool:
        """Check if variable is set."""
        raise NotImplementedError

    @property
    def name(self) -> str:
        """Get variable name."""
        raise NotImplementedError

    def get_masked_value(self) -> str:
        """Get masked value for display."""
        raise NotImplementedError


def validate_and_categorize_var(
    var_config: VarConfigProtocol,
    *,
    verbose: bool,
    success_list: list[Any],
    missing_list: list[Any],
    format_func: Any,
) -> None:
    """Validate a single variable and categorize it.

    Args:
        var_config: Variable configuration to validate
        verbose: Whether to print status
        success_list: List to append to if variable is set
        missing_list: List to append to if variable is missing
        format_func: Function to format missing message (success/warning/error)
    """
    if var_config.is_set:
        success_list.append(var_config)
        if verbose:
            masked = var_config.get_masked_value()
            print(f"  {success(f'{var_config.name}: {masked}')}")
    else:
        missing_list.append(var_config)
        if verbose:
            desc = getattr(var_config, "description", "")
            print(f"  {format_func(f'{var_config.name}: NOT SET - {desc}')}")


def create_error_result(
    error_msg: ErrorMessage,
    *,
    verbose: bool,
    **result_kwargs: Any,
) -> dict[str, Any]:
    """Create error result dictionary consistently.

    Args:
        error_msg: Error message
        verbose: Whether to print error
        **result_kwargs: Additional result fields

    Returns:
        Dictionary with passed=False, errors, and additional fields
    """
    if verbose:
        print(error(error_msg))

    return {
        "passed": False,
        "errors": (error_msg,),
        **result_kwargs,
    }


__all__: list[str] = [
    "VarConfigProtocol",
    "validate_and_categorize_var",
    "create_error_result",
]
