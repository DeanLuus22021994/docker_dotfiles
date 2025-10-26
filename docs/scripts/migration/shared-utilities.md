---
date_created: "2025-10-26T18:32:25.988029+00:00"
last_updated: "2025-10-26T18:32:25.988029+00:00"
tags: ["documentation", "scripts", "automation"]
description: "Documentation for shared utilities"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- scripts
- python
- utilities
  description: Shared Python utilities for DRY code practices
  ---\n# Shared Utilities (DRY)

Shared utilities eliminate code duplication across Python scripts.

## Colors (`python/utils/colors.py`)

```python
from python.utils.colors import success, error, warning, info

print(success("✓ Task completed"))
print(error("✗ Task failed"))
print(warning("⚠ Warning message"))
print(info("ℹ Information"))
```

**Benefits:** Consistent colored output, automatic terminal detection.

## File Operations (`python/utils/file_utils.py`)

```python
from python.utils.file_utils import read_json, write_json, ensure_dir

config = read_json('config.json')
ensure_dir('logs/')
write_json('output.json', data)
```

**Features:** Error handling, path validation, atomic writes.

## Logging (`python/utils/logging_utils.py`)

```python
from python.utils.logging_utils import setup_logger

logger = setup_logger(__name__, use_colors=True)
logger.info("Processing started")
logger.error("Task failed")
```

**Features:** Colored output, file logging, structured format.

## Usage Pattern

Add parent directory to Python path:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Now import utilities
from python.utils.colors import success
from python.utils.file_utils import read_json
```

See `scripts/python/utils/README.md` for full API documentation.
