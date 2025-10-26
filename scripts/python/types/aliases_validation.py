"""Type aliases specific to validation modules."""

from typing import Literal, TypeAlias

EnvVarName: TypeAlias = str
EnvVarValue: TypeAlias = str
ConfigType: TypeAlias = Literal["yaml", "json", "nginx", "postgresql", "mariadb"]

__all__: list[str] = ["EnvVarName", "EnvVarValue", "ConfigType"]
