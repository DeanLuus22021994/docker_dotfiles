---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["python", "type-hints", "pep-585", "modernization"]
description: "Python 3.14 type hints and PEP 585 built-in generics"
---
# Python 3.14 Type Hints

Modern type hints using PEP 585 built-in generics.

## Old vs New Syntax

**Old (Python 3.8, deprecated):**
```python
from typing import List, Dict, Tuple, Optional

def process(items: List[str]) -> Dict[str, int]:
    result: Dict[str, int] = {}
    optional: Optional[str] = None
```

**New (Python 3.14, preferred):**
```python
def process(items: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    optional: str | None = None
```

## Built-in Generic Types

- `list[T]` instead of `List[T]`
- `dict[K, V]` instead of `Dict[K, V]`
- `tuple[T, ...]` instead of `Tuple[T, ...]`
- `set[T]` instead of `Set[T]`
- `frozenset[T]` instead of `FrozenSet[T]`
- `type[T]` instead of `Type[T]`

## Union Types

```python
# Old
from typing import Union
value: Union[int, str] = 42

# New
value: int | str = 42
```

## Optional Types

```python
# Old
from typing import Optional
name: Optional[str] = None

# New
name: str | None = None
```

## Migration

Run automated conversion:
```bash
pyupgrade --py314-plus **/*.py
```

Update imports:
```python
# Remove deprecated imports
# from typing import List, Dict, Tuple, Optional

# Keep for advanced types
from typing import Protocol, TypedDict, Literal
```
