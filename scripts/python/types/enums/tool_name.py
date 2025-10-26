"""Code quality tool enumeration."""

from enum import StrEnum


class QualityTool(StrEnum):
    """Code quality checking tools."""

    BLACK = "black"
    RUFF = "ruff"
    MYPY = "mypy"
    PYLINT = "pylint"
    YAMLLINT = "yamllint"
    PYTEST = "pytest"


__all__: list[str] = ["QualityTool"]
