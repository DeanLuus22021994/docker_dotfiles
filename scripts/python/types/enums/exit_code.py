"""Exit code enumeration for script returns."""

from enum import IntEnum


class ExitCode(IntEnum):
    """Standard exit codes for scripts."""

    SUCCESS = 0
    FAILURE = 1
    INVALID_USAGE = 2
    NOT_FOUND = 127


__all__: list[str] = ["ExitCode"]
