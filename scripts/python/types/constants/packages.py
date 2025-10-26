"""Package and dependency constants."""

from typing import Final

REQUIRED_PACKAGES: Final[tuple[str, ...]] = (
    "black",
    "ruff",
    "mypy",
    "yamllint",
    "pytest",
)

__all__: list[str] = ["REQUIRED_PACKAGES"]
