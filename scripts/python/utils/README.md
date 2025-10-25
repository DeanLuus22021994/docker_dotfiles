# Utils Module

Shared utility modules following DRY (Don't Repeat Yourself) principles for consistent functionality across all Python scripts.

## Overview

The utils module provides reusable components for terminal formatting, file operations, and logging configuration. These utilities ensure consistent behavior and reduce code duplication.

## Modules

### colors.py

**Purpose:** ANSI terminal colors and formatting functions for consistent output

**Usage:**

```python
from python.utils.colors import Colors, success, error, warning, info, header, separator

# Using Colors class directly
print(f"{Colors.GREEN}Success!{Colors.RESET}")
print(f"{Colors.RED}Error!{Colors.RESET}")
print(f"{Colors.BOLD}{Colors.BLUE}Header{Colors.RESET}")

# Using helper functions (recommended)
print(success("Operation completed"))  # ✓ Operation completed
print(error("Something went wrong"))   # ✗ Something went wrong
print(warning("Please review this"))   # ⚠ Please review this
print(info("Processing..."))           # ℹ Processing...
print(header("=== Section Title ==="))
print(separator())                     # === separator line ===
```

**Available Functions:**

- `colorize(text, color)` - Wrap text with ANSI color codes
- `success(text)` - Green checkmark message (✓)
- `error(text)` - Red X message (✗)
- `warning(text)` - Yellow warning message (⚠)
- `info(text)` - Blue info message (ℹ)
- `bold(text)` - Bold text
- `header(text)` - Bold blue header
- `separator(width, char)` - Bold separator line

**Colors Class:**

```python
Colors.BLACK, Colors.RED, Colors.GREEN, Colors.YELLOW
Colors.BLUE, Colors.MAGENTA, Colors.CYAN, Colors.WHITE
Colors.BOLD, Colors.UNDERLINE, Colors.RESET
```

**Example Output:**

```
✓ Database connection successful
✗ Failed to read configuration file
⚠ Resource usage above 80%
ℹ Processing 156 files...
=== Starting Deployment ===
============================================================
```

---

### file_utils.py

**Purpose:** Cross-platform file operation helpers with type-safe interfaces

**Usage:**

```python
from python.utils.file_utils import (
    read_json, write_json, read_lines,
    file_exists, ensure_dir, get_files_by_extension,
    get_file_size, get_relative_path
)

# JSON operations
config: dict[str, Any] = read_json('.config/settings.json')
write_json('output.json', {'key': 'value'}, indent=2)

# File operations
lines: list[str] = read_lines('config.txt', strip=True)
exists: bool = file_exists('.env')
size: int = get_file_size('large_file.bin')

# Directory operations
ensure_dir('logs/')  # Creates if doesn't exist
py_files: list[Path] = get_files_by_extension('.', '.py', recursive=True)
rel_path: str = get_relative_path('/abs/path/file.txt', '/abs')
```

**Available Functions:**

- `read_json(file_path) -> dict[str, Any]` - Parse JSON file
- `write_json(file_path, data, indent=2) -> None` - Write JSON file
- `read_lines(file_path, strip=True) -> list[str]` - Read file lines
- `file_exists(file_path) -> bool` - Check file existence
- `ensure_dir(dir_path) -> None` - Create directory if needed
- `get_files_by_extension(directory, extension, recursive=True) -> list[Path]` - Find files
- `get_file_size(file_path) -> int` - Get file size in bytes
- `get_relative_path(file_path, base_path) -> str` - Calculate relative path

**Error Handling:**

- `FileNotFoundError` - File doesn't exist
- `json.JSONDecodeError` - Invalid JSON format
- `PermissionError` - Insufficient permissions
- `OSError` - File system errors

**Type Safety:**

All functions use Python 3.14 type hints:

```python
def read_json(file_path: str) -> dict[str, Any]: ...
def get_files_by_extension(directory: str, extension: str, recursive: bool = True) -> list[Path]: ...
```

---

### logging_utils.py

**Purpose:** Centralized logging configuration with color-coded output support

**Usage:**

```python
from python.utils.logging_utils import setup_logger, get_logger, ColoredFormatter

# Setup logger with colors
logger = setup_logger('my_script', use_colors=True)

# Use logger
logger.debug("Debug information")
logger.info("Processing started")
logger.warning("Resource usage high")
logger.error("Operation failed")
logger.critical("System failure")

# Get existing logger
logger = get_logger('my_script')

# Custom formatter
formatter = ColoredFormatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    use_colors=True
)
```

**Available Functions:**

- `setup_logger(name, level=INFO, format_string=None, use_colors=True)` - Configure new logger
- `get_logger(name)` - Retrieve existing logger
- `ColoredFormatter` - Custom formatter with ANSI color support

**Log Levels:**

```python
logging.DEBUG    # Detailed diagnostic information
logging.INFO     # General informational messages
logging.WARNING  # Warning messages (potential issues)
logging.ERROR    # Error messages (operation failed)
logging.CRITICAL # Critical errors (system failure)
```

**Color Scheme:**

- `DEBUG` - Cyan
- `INFO` - Green
- `WARNING` - Yellow
- `ERROR` - Red
- `CRITICAL` - Red + Bold

**Example Output:**

```
2025-10-25 14:30:15 - validator - INFO - Starting validation
2025-10-25 14:30:16 - validator - WARNING - Missing optional env var
2025-10-25 14:30:17 - validator - ERROR - Configuration file invalid
```

---

## Module API

### Import Patterns

```python
# Import entire modules
from python.utils import colors, file_utils, logging_utils

# Import specific functions
from python.utils.colors import success, error
from python.utils.file_utils import read_json, ensure_dir
from python.utils.logging_utils import setup_logger

# Wildcard import (via __all__)
from python.utils import *
```

### Exports

The module exports the following via `__all__`:

- `colors` - Terminal color formatting module
- `file_utils` - File operation utilities module
- `logging_utils` - Logging configuration module

---

## Type Annotations

All utilities use modern Python 3.14 type hints with built-in generics:

```python
# colors.py
def colorize(text: str, color: str) -> str: ...
def success(text: str) -> str: ...

# file_utils.py
def read_json(file_path: str) -> dict[str, Any]: ...
def read_lines(file_path: str, strip: bool = True) -> list[str]: ...
def get_files_by_extension(directory: str, extension: str, recursive: bool = True) -> list[Path]: ...

# logging_utils.py
def setup_logger(name: str, level: int = logging.INFO, format_string: Optional[str] = None, use_colors: bool = True) -> logging.Logger: ...
```

---

## Dependencies

**Standard Library Only:**

- `json` - JSON parsing
- `os` - Operating system interface
- `pathlib` - Object-oriented filesystem paths
- `logging` - Logging facility
- `sys` - System-specific parameters

**No External Dependencies Required!**

---

## Best Practices

### Using Colors

```python
# ✓ Good - Use helper functions
print(success("Task completed"))
print(error("Task failed"))

# ✗ Avoid - Manual color codes
print(f"{Colors.GREEN}✓{Colors.RESET} Task completed")
```

### File Operations

```python
# ✓ Good - Handle errors
try:
    config = read_json('config.json')
except FileNotFoundError:
    config = {}  # Use defaults

# ✓ Good - Ensure directory exists
ensure_dir('logs/')
write_json('logs/output.json', data)
```

### Logging

```python
# ✓ Good - Setup once at module level
logger = setup_logger(__name__)

def main():
    logger.info("Starting process")
    try:
        # Do work
        logger.info("Process completed")
    except Exception as e:
        logger.error(f"Process failed: {e}")
```

---

## Examples

### Complete Script Template

```python
#!/usr/bin/env python3
"""
Example script using all utilities
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from python.utils.colors import success, error, warning, header, separator
from python.utils.file_utils import read_json, ensure_dir, file_exists
from python.utils.logging_utils import setup_logger

# Setup logging
logger = setup_logger(__name__, use_colors=True)

def main() -> int:
    """Main function"""
    print(separator())
    print(header("Starting Process"))
    print(separator())

    try:
        # Check configuration
        if not file_exists('config.json'):
            print(warning("Config not found, using defaults"))
            config = {}
        else:
            config = read_json('config.json')
            logger.info("Configuration loaded")

        # Ensure output directory
        ensure_dir('output/')

        # Do work
        logger.info("Processing data...")
        # ... processing logic ...

        print(success("Process completed successfully"))
        return 0

    except Exception as e:
        logger.error(f"Process failed: {e}")
        print(error(f"Failed: {e}"))
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

---

## Standards Compliance

### Python 3.14

- ✅ PEP 585: Built-in generics (`list[str]`, `dict[str, Any]`)
- ✅ PEP 649: Deferred annotation evaluation
- ✅ PEP 484: Type hints on all functions
- ✅ PEP 8: Code style compliance

### Code Quality

- ✅ Black formatting (line-length=100)
- ✅ Ruff linting (strict mode)
- ✅ mypy type checking (strict mode)
- ✅ Zero external dependencies

---

## Troubleshooting

### Import errors

Ensure parent directory is in Python path:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

### Colors not displaying

- Check terminal supports ANSI colors
- Windows: Use Windows Terminal or enable ANSI support
- Disable colors: `use_colors=False` in logging

### File encoding issues

All file operations use UTF-8 encoding by default:

```python
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
```

---

**Last Updated:** 2025-10-25  
**Python Version:** 3.14.0+  
**Module Version:** 1.0.0
