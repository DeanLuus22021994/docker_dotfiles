"""Base checker class with common subprocess handling."""

import subprocess
from abc import ABC, abstractmethod
from collections.abc import Sequence

from python.types.aliases import ErrorMessage


class BaseCommandChecker(ABC):
    """Base class for checkers that run external commands.

    Eliminates duplicate subprocess boilerplate across audit/validation modules.
    """

    def __init__(self, *, verbose: bool = True) -> None:
        """Initialize checker.

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose

    @abstractmethod
    def get_command(self) -> Sequence[str]:
        """Get the command to execute.

        Returns:
            Command as sequence of strings
        """
        raise NotImplementedError

    def run_subprocess(self, args: Sequence[str], *, check: bool = False) -> tuple[int, str, str]:
        """Run subprocess and capture output.

        Args:
            args: Command arguments
            check: Whether to raise on non-zero exit

        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        try:
            result = subprocess.run(args, capture_output=True, text=True, check=check)
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout or "", e.stderr or ""
        except FileNotFoundError:
            return 127, "", f"Command not found: {args[0]}"

    def parse_errors(self, stderr: str) -> tuple[ErrorMessage, ...]:
        """Parse stderr into error messages.

        Override in subclasses for tool-specific parsing.

        Args:
            stderr: Standard error output

        Returns:
            Tuple of error messages
        """
        if not stderr:
            return ()
        return tuple(line.strip() for line in stderr.split("\n") if line.strip())


__all__: list[str] = ["BaseCommandChecker"]
