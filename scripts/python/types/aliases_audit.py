"""Type aliases specific to audit modules."""

from typing import TypeAlias

ToolName: TypeAlias = str
PackageName: TypeAlias = str
Version: TypeAlias = str

__all__: list[str] = ["ToolName", "PackageName", "Version"]
