# Python Scripts

Python automation scripts organized by task (SRP/DRY principles).

## Structure

```
python/
├── README.md                # This file - overview and quick reference
├── __init__.py              # Package marker
├── audit/                   # Code quality auditing
│   ├── README.md            # Detailed audit module documentation
│   ├── __init__.py          # Package exports
│   ├── code_quality.py      # Black, Ruff, mypy checks
│   └── dependencies.py      # Package audit and outdated check
├── validation/              # Configuration validation
│   ├── README.md            # Detailed validation module documentation
│   ├── __init__.py          # Package exports
│   ├── validate_env.py      # Environment variables validation
│   └── validate_configs.py  # Config files validation
└── utils/                   # Shared utilities (DRY)
    ├── README.md            # Detailed utils module documentation
    ├── __init__.py          # Package exports
    ├── colors.py            # ANSI color codes
    ├── file_utils.py        # File operations
    └── logging_utils.py     # Logging configuration
```

## Quick Links

- **[Audit Module](audit/README.md)** - Code quality checks and dependency auditing
- **[Validation Module](validation/README.md)** - Environment and configuration validation
- **[Utils Module](utils/README.md)** - Shared utilities (colors, files, logging)

## Usage

### Via Orchestrator (Recommended)

```powershell
# PowerShell
..\orchestrator.ps1 validate env
..\orchestrator.ps1 validate configs
..\orchestrator.ps1 audit code
..\orchestrator.ps1 audit deps

# Bash
../orchestrator.sh validate env
../orchestrator.sh audit code

# Python
python ..\orchestrator.py validate env
python ..\orchestrator.py validate configs
python ..\orchestrator.py audit code
python ..\orchestrator.py audit deps
```

### Direct Execution

```powershell
# Windows
python validation\validate_env.py
python validation\validate_configs.py

# Linux/macOS
python3 validation/validate_env.py
python3 validation/validate_configs.py
```

## Modules Overview

### Audit Module

**Purpose:** Code quality auditing and dependency management
**Documentation:** [audit/README.md](audit/README.md)

**Scripts:**

- `code_quality.py` - Black, Ruff, mypy checks
- `dependencies.py` - Outdated packages and dependency validation

**Quick Start:**

```powershell
python ../orchestrator.py audit code
python ../orchestrator.py audit deps
```

---

### Validation Module

**Purpose:** Environment and configuration validation before deployment
**Documentation:** [validation/README.md](validation/README.md)

**Scripts:**

- `validate_env.py` - Environment variables validation
- `validate_configs.py` - YAML, JSON, nginx, database config validation

**Quick Start:**

```powershell
python ../orchestrator.py validate env
python ../orchestrator.py validate configs
```

---

### Utils Module

**Purpose:** Shared utilities following DRY principles
**Documentation:** [utils/README.md](utils/README.md)

**Modules:**

- `colors.py` - Terminal color formatting
- `file_utils.py` - File operations
- `logging_utils.py` - Logging configuration

**Quick Start:**

```python
from python.utils.colors import success, error
from python.utils.file_utils import read_json
from python.utils.logging_utils import setup_logger
```

## Common Usage Patterns

### Running Validations

```powershell
# Before starting Docker stack
python ../orchestrator.py validate env      # Check environment variables
python ../orchestrator.py validate configs  # Validate configuration files
```

### Running Audits

```powershell
# Before committing code
python ../orchestrator.py audit code  # Black, Ruff, mypy checks
python ../orchestrator.py audit deps  # Check outdated packages
```

### Using Utilities

```python
# Terminal colors
from python.utils.colors import success, error, warning

print(success("Operation completed"))  # ✓ Operation completed
print(error("Something failed"))       # ✗ Something failed

# File operations
from python.utils.file_utils import read_json, ensure_dir

config = read_json('config.json')
ensure_dir('logs/')

# Logging
from python.utils.logging_utils import setup_logger

logger = setup_logger(__name__, use_colors=True)
logger.info("Processing started")
```

For detailed documentation, see individual module READMEs:

- [Audit Module Documentation](audit/README.md)
- [Validation Module Documentation](validation/README.md)
- [Utils Module Documentation](utils/README.md)

## Adding New Scripts

### 1. Create Script

```python
#!/usr/bin/env python3
"""
Script description
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from python.utils.colors import success, error, warning
from python.utils.file_utils import read_json, file_exists

def main():
    """Main function"""
    try:
        # Do work
        print(success("Task completed"))
        return 0
    except Exception as e:
        print(error(f"Task failed: {e}"))
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

### 2. Add to Orchestrator

Update `../orchestrator.py`:

```python
elif task == 'new_category':
    if action == 'new_action':
        script = SCRIPT_DIR / 'python' / 'category' / 'script.py'
        # Execute script
```

### 3. Update README

Add to scripts reference table.

### 4. Test

```powershell
# Direct
python category\script.py

# Via orchestrator
python ..\orchestrator.py category action
```

## Best Practices

### Imports

```python
# Standard library
import os
import sys
from typing import List, Dict, Tuple
from pathlib import Path

# Add parent to path (for scripts/ imports)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Local imports
from python.utils.colors import success, error
```

### Error Handling

```python
def main():
    try:
        # Do work
        return 0
    except FileNotFoundError as e:
        print(error(f"File not found: {e}"))
        return 1
    except Exception as e:
        print(error(f"Unexpected error: {e}"))
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

### Type Hints

```python
def validate_env_vars() -> Tuple[bool, List[str], List[str]]:
    """Validate environment variables"""
    missing: List[str] = []
    # ...
    return all_valid, missing_required, missing_optional
```

### Exit Codes

- `0` = Success
- `1` = Error
- Use `sys.exit(code)` consistently

## Python Environment

**Requirements:**

- Python 3.14.0+ (recommended, 3.8+ compatible)
- UV package manager (optional, recommended for faster installs)
- Core Dependencies: `yamllint`, `black`, `ruff`, `mypy`, `pytest`

**Setup:**

```powershell
# Install Python 3.14.0 from python.org (NOT Microsoft Store)
# Disable Windows App Execution Aliases

# Install UV
pip install uv

# Install dependencies
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

**Troubleshooting:** See [Python Setup Guide](../../docs/python-setup-troubleshooting.md)

## Code Quality

### Black Formatting

```powershell
# Format all Python files
black scripts/python/

# Check formatting
black --check scripts/python/
```

### Ruff Linting

```powershell
# Lint all files
ruff check scripts/python/

# Auto-fix issues
ruff check --fix scripts/python/
```

### Mypy Type Checking

```powershell
# Type check (strict mode)
mypy --strict scripts/python/validation/
```

## Testing

```python
# Unit tests (planned)
pytest tests/python/

# Integration tests
python validation/validate_env.py
python validation/validate_configs.py
```

## Python 3.14 Compliance

All modules follow modern Python 3.14 best practices:

- ✅ **PEP 585**: Built-in generics (`list[str]`, `dict[str, Any]`, `tuple[bool, list[str]]`)
- ✅ **PEP 649**: Deferred annotation evaluation
- ✅ **PEP 484**: Type hints on all functions
- ✅ **Explicit exports**: Type-annotated `__all__: list[str] = [...]` in all `__init__.py` files
- ✅ **Proper imports**: Relative imports before `__all__` declarations

**Example:**

```python
# Package imports work as expected
from python.audit import code_quality, dependencies
from python.validation import validate_env, validate_configs
from python.utils import colors, file_utils, logging_utils

# Wildcard imports (via __all__)
from python.audit import *
```

## Documentation

Each module has comprehensive documentation:

| Module         | Purpose                            | Documentation                                |
| -------------- | ---------------------------------- | -------------------------------------------- |
| **audit**      | Code quality and dependency checks | [audit/README.md](audit/README.md)           |
| **validation** | Environment and config validation  | [validation/README.md](validation/README.md) |
| **utils**      | Shared utilities (DRY)             | [utils/README.md](utils/README.md)           |

---

**Last Updated:** 2025-10-25
**Python Version:** 3.14.0+
**Status:** Enterprise-Grade Certified ✓
