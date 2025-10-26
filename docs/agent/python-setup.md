---
date_created: "2025-10-26T18:32:25.939992+00:00"
last_updated: "2025-10-26T18:32:25.939992+00:00"
tags: ["documentation", "agent", "development", "python"]
description: "Documentation for python setup"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- python
- environment
- setup
  description: Python 3.14 environment setup for development scripts
  ---\n# Python Environment Setup

## Required Version

- **Python 3.14.0+** for all scripts
- **UV package manager** for dependency management
- **NOT** Microsoft Store Python (causes PATH issues)

## Setup (Windows)

```powershell
# 1. Install Python 3.14.0 from python.org
# 2. Disable Windows App Execution Aliases:
#    Settings → Apps → Advanced app settings → App execution aliases
#    Disable: "App Installer python.exe" and "python3.exe"

# 3. Verify installation
python --version  # Should show Python 3.14.0
where.exe python  # Should NOT show AppData\Local\Microsoft

# 4. Install UV
pip install uv

# 5. Install dependencies
uv pip install -r requirements.txt
```

## Shared Utilities (DRY)

- **`python/utils/colors.py`**: ANSI color codes
- **`python/utils/file_utils.py`**: File operations
- **`python/utils/logging_utils.py`**: Logging config

Import from `scripts.python.utils` to avoid code duplication.

See [configuration management guide](agent-configuration.md) for config details.
