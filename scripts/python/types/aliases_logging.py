"""Type aliases for logging."""

from typing import Literal, TypeAlias

LogLevel: TypeAlias = int
LogLevelName: TypeAlias = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
FormatString: TypeAlias = str
LoggerName: TypeAlias = str

__all__: list[str] = ["LogLevel", "LogLevelName", "FormatString", "LoggerName"]
