# Python Scripts

Python automation scripts organized by task (SRP/DRY principles).

## Structure

```
python/
├── __init__.py              # Package marker
├── validation/              # Configuration validation
│   ├── validate_env.py      # Environment variables validation
│   └── validate_configs.py  # Config files validation
├── audit/                   # Code audit scripts (planned)
└── utils/                   # Shared utilities (DRY)
    ├── __init__.py
    ├── colors.py            # ANSI color codes
    ├── file_utils.py        # File operations
    └── logging_utils.py     # Logging configuration
```

## Usage

### Via Orchestrator (Recommended)

```powershell
# PowerShell
..\orchestrator.ps1 validate env
..\orchestrator.ps1 validate configs

# Bash
../orchestrator.sh validate env

# Python
python ..\orchestrator.py validate env
python ..\orchestrator.py validate configs
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

## Scripts Reference

### validation/validate_env.py
**Purpose:** Validate environment variables before Docker stack startup  
**Usage:** `python validate_env.py`  
**Exit Code:** 0 = all required vars set, 1 = missing vars  
**Dependencies:** None (uses shared colors utility)

**Checks:**
- Required: `GITHUB_OWNER`, `GH_PAT`, `DOCKER_*_PASSWORD`, etc.
- Optional: `DOCKER_ACCESS_TOKEN`, `CODECOV_TOKEN`

### validation/validate_configs.py
**Purpose:** Validate configuration files (YAML, JSON, nginx, databases)  
**Usage:** `python validate_configs.py`  
**Exit Code:** 0 = all configs valid, 1 = validation errors  
**Dependencies:** `yamllint`, `docker` (for nginx validation)

**Validates:**
- YAML files (docker-compose, GitHub workflows)
- JSON files (excluding .vscode JSONC)
- nginx configs (via Docker test)
- PostgreSQL config (syntax check)
- MariaDB config (syntax check)

## Shared Utilities (DRY)

### utils/colors.py

ANSI terminal colors for consistent output:

```python
from python.utils.colors import Colors, success, error, warning, info, header, separator

# Direct use
print(f"{Colors.GREEN}Success!{Colors.RESET}")
print(f"{Colors.RED}Error!{Colors.RESET}")

# Helper functions (recommended)
print(success("Operation completed"))  # ✓ Operation completed
print(error("Something went wrong"))   # ✗ Something went wrong
print(warning("Please review this"))   # ⚠ Please review this
print(info("Processing..."))           # ℹ Processing...
print(header("=== Section ==="))       # Bold blue header
print(separator())                     # Bold === line
```

**Available:**
- `Colors` class: GREEN, RED, YELLOW, BLUE, BOLD, RESET, etc.
- `colorize(text, color)`: Wrap text with color
- `success(text)`: Green checkmark message
- `error(text)`: Red X message
- `warning(text)`: Yellow warning message
- `info(text)`: Blue info message
- `header(text)`: Bold blue header
- `separator(width, char)`: Bold separator line

### utils/file_utils.py

File operations helpers:

```python
from python.utils.file_utils import (
    read_json, write_json, read_lines,
    file_exists, ensure_dir, get_files_by_extension
)

# JSON operations
data = read_json('.config/settings.json')
write_json('output.json', {'key': 'value'})

# File operations
lines = read_lines('config.txt', strip=True)
if file_exists('.env'):
    # Do something

# Directory operations
ensure_dir('logs/')  # Create if not exists
py_files = get_files_by_extension('.', '.py', recursive=True)
```

**Available:**
- `read_json(path)`: Parse JSON file
- `write_json(path, data, indent)`: Write JSON
- `read_lines(path, strip)`: Read file lines
- `file_exists(path)`: Check file existence
- `ensure_dir(path)`: Create directory if needed
- `get_files_by_extension(dir, ext, recursive)`: Find files
- `get_file_size(path)`: Get file size in bytes
- `get_relative_path(path, base)`: Get relative path

### utils/logging_utils.py

Logging configuration with color support:

```python
from python.utils.logging_utils import setup_logger

# Setup logger
logger = setup_logger('my_script', use_colors=True)

# Use logger
logger.debug("Debug info")
logger.info("Processing started")
logger.warning("Resource usage high")
logger.error("Operation failed")
logger.critical("System failure")
```

**Available:**
- `setup_logger(name, level, format_string, use_colors)`: Configure logger
- `get_logger(name)`: Get existing logger
- `ColoredFormatter`: Custom formatter with ANSI colors

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
- Python 3.13+ (3.8+ compatible)
- UV package manager (recommended)
- Dependencies: `yamllint`, `black`, `ruff`, `mypy`

**Setup:**

```powershell
# Install Python 3.13 from python.org (NOT Microsoft Store)
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

## Planned Scripts

- `audit/code_quality.py` - Automated code quality checks
- `audit/security_scan.py` - Security vulnerability scanning
- `utils/docker_utils.py` - Docker API helpers
- `utils/git_utils.py` - Git operations helpers

---

**Last Updated:** 2025-10-25 (v3.0 refactor - DRY utilities extracted)
