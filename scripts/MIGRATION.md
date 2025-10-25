# Scripts Migration Guide

**Version:** 3.0.0  
**Date:** 2025-10-25  
**Status:** Complete

---

## Overview

This guide documents the migration from the old flat scripts structure to the new organized structure following SRP (Single Responsibility Principle) and DRY (Don't Repeat Yourself) principles.

---

## What Changed

### Old Structure (Deprecated)

```
scripts/
├── apply-settings.ps1
├── setup_secrets.ps1
├── start_devcontainer.ps1
├── start_devcontainer.sh
├── serve_docs.ps1
├── serve_docs.sh
├── test_integration.ps1
├── validate_env.py
└── validate_configs.py
```

### New Structure (Current)

```
scripts/
├── README.md                    # Main scripts documentation
├── orchestrator.ps1             # PowerShell orchestrator
├── orchestrator.sh              # Bash orchestrator
├── orchestrator.py              # Python orchestrator
├── powershell/
│   ├── README.md
│   ├── config/
│   │   ├── apply-settings.ps1
│   │   └── setup-secrets.ps1
│   ├── docker/
│   │   └── start-devcontainer.ps1
│   ├── docs/
│   │   └── serve-docs.ps1
│   └── audit/
│       └── test-integration.ps1
├── python/
│   ├── README.md
│   ├── __init__.py
│   ├── validation/
│   │   ├── README.md            # Detailed validation docs
│   │   ├── __init__.py
│   │   ├── validate_env.py
│   │   └── validate_configs.py
│   ├── audit/
│   │   ├── README.md            # Detailed audit docs
│   │   ├── __init__.py
│   │   ├── code_quality.py
│   │   └── dependencies.py
│   └── utils/
│       ├── README.md            # Detailed utils docs
│       ├── __init__.py
│       ├── colors.py
│       ├── file_utils.py
│       └── logging_utils.py
└── bash/
    ├── README.md
    ├── docker/
    │   └── start-devcontainer.sh
    └── docs/
        └── serve-docs.sh
```

---

## Migration Path Mapping

| Old Path                         | New Path                                           | Notes       |
| -------------------------------- | -------------------------------------------------- | ----------- |
| `scripts/validate_env.py`        | `scripts/python/validation/validate_env.py`        | ✅ Migrated |
| `scripts/validate_configs.py`    | `scripts/python/validation/validate_configs.py`    | ✅ Migrated |
| `scripts/apply-settings.ps1`     | `scripts/powershell/config/apply-settings.ps1`     | ✅ Migrated |
| `scripts/setup_secrets.ps1`      | `scripts/powershell/config/setup-secrets.ps1`      | ✅ Migrated |
| `scripts/start_devcontainer.ps1` | `scripts/powershell/docker/start-devcontainer.ps1` | ✅ Migrated |
| `scripts/serve_docs.ps1`         | `scripts/powershell/docs/serve-docs.ps1`           | ✅ Migrated |
| `scripts/test_integration.ps1`   | `scripts/powershell/audit/test-integration.ps1`    | ✅ Migrated |
| `scripts/start_devcontainer.sh`  | `scripts/bash/docker/start-devcontainer.sh`        | ✅ Migrated |
| `scripts/serve_docs.sh`          | `scripts/bash/docs/serve-docs.sh`                  | ✅ Migrated |

---

## How to Migrate Your Code

### Option 1: Use Orchestrators (Recommended)

The new orchestrators provide a unified interface across all platforms:

**Before:**

```powershell
# Old direct calls
python scripts/validate_env.py
python scripts/validate_configs.py
```

**After:**

```powershell
# Via orchestrator (works on Windows, Linux, macOS)
python scripts/orchestrator.py validate env
python scripts/orchestrator.py validate configs

# Or PowerShell-specific
scripts/orchestrator.ps1 validate env

# Or Bash-specific
scripts/orchestrator.sh validate env
```

### Option 2: Update Direct Paths

If you prefer direct script execution:

**Before:**

```powershell
python scripts/validate_env.py
```

**After:**

```powershell
python scripts/python/validation/validate_env.py
```

---

## Updated References

### Makefile

**Before:**

```makefile
validate-env:
	@python scripts/validate_env.py
```

**After:**

```makefile
validate-env:
	@python scripts/python/validation/validate_env.py
```

**Status:** ✅ Already updated

---

### GitHub Actions Workflows

**Before:**

```yaml
- name: Check required environment variables
  run: python scripts/validate_env.py
```

**After:**

```yaml
- name: Check required environment variables
  run: python scripts/python/validation/validate_env.py
```

**Status:** ✅ Already updated in `.github/workflows/validate.yml`

---

### Import Statements (Python)

**Before:**

```python
# Old: Colors duplicated in multiple files
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    # ...
```

**After:**

```python
# New: Shared utilities (DRY)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from python.utils.colors import success, error, warning
from python.utils.file_utils import read_json, ensure_dir
from python.utils.logging_utils import setup_logger
```

---

## New Features

### 1. Orchestrators

Unified task execution across platforms:

```powershell
# List all available tasks
scripts/orchestrator.ps1 help

# Execute tasks
scripts/orchestrator.ps1 validate env
scripts/orchestrator.ps1 validate configs
scripts/orchestrator.ps1 audit code
scripts/orchestrator.ps1 audit deps
```

### 2. Shared Utilities (DRY)

**Colors (`python/utils/colors.py`):**

```python
from python.utils.colors import success, error, warning, info

print(success("✓ Task completed"))
print(error("✗ Task failed"))
print(warning("⚠ Warning message"))
print(info("ℹ Information"))
```

**File Operations (`python/utils/file_utils.py`):**

```python
from python.utils.file_utils import read_json, write_json, ensure_dir

config = read_json('config.json')
ensure_dir('logs/')
write_json('output.json', data)
```

**Logging (`python/utils/logging_utils.py`):**

```python
from python.utils.logging_utils import setup_logger

logger = setup_logger(__name__, use_colors=True)
logger.info("Processing started")
logger.error("Task failed")
```

### 3. Module-Specific Documentation

Each module now has comprehensive documentation:

- `scripts/python/audit/README.md` - Code quality and dependency auditing
- `scripts/python/validation/README.md` - Environment and config validation
- `scripts/python/utils/README.md` - Shared utilities

### 4. Python 3.14 Compliance

All Python code uses modern type hints:

```python
# Old (Python 3.8 style)
from typing import List, Tuple, Dict

def check_packages() -> Tuple[bool, List[str]]:
    errors: List[str] = []

# New (Python 3.14 style)
def check_packages() -> tuple[bool, list[str]]:
    errors: list[str] = []
```

---

## Breaking Changes

### 1. Direct Script Paths

❌ **Old paths no longer work:**

```powershell
python scripts/validate_env.py  # File not found
```

✅ **Use new paths:**

```powershell
python scripts/python/validation/validate_env.py
```

### 2. Import Paths (Python)

❌ **Old imports won't work:**

```python
from validate_env import Colors  # Module not found
```

✅ **Use package imports:**

```python
from python.utils.colors import Colors, success, error
```

### 3. Script Locations in CI/CD

Update all CI/CD pipelines, makefiles, and automation scripts to use new paths.

---

## Backward Compatibility

### Orchestrators Provide Compatibility Layer

The orchestrators handle path translation automatically:

```powershell
# Works with new structure
scripts/orchestrator.ps1 validate env

# Internally calls:
# python scripts/python/validation/validate_env.py
```

### Deprecated Scripts

Old scripts in `scripts/` root have been removed. If you need them:

1. Update to use orchestrators (recommended)
2. Update paths to new locations
3. Check git history if you need old versions

---

## Migration Checklist

Use this checklist to migrate your project:

### For Developers

- [ ] Update local scripts to use new paths
- [ ] Replace direct imports with package imports
- [ ] Use shared utilities instead of duplicating code
- [ ] Update documentation references
- [ ] Test scripts with new structure

### For CI/CD Pipelines

- [ ] Update GitHub Actions workflow paths
- [ ] Update GitLab CI/CD script paths
- [ ] Update Jenkins pipeline scripts
- [ ] Update Azure DevOps pipeline tasks
- [ ] Update any automation scripts

### For Documentation

- [ ] Update README.md references
- [ ] Update setup guides
- [ ] Update troubleshooting docs
- [ ] Update API documentation
- [ ] Update contribution guidelines

### For Makefiles/Build Scripts

- [ ] Update Makefile targets (✅ Done)
- [ ] Update package.json scripts
- [ ] Update build automation
- [ ] Update deployment scripts

---

## Examples

### Example 1: Running Validation

**Before:**

```bash
# Direct execution
python scripts/validate_env.py
python scripts/validate_configs.py
```

**After (Orchestrator - Recommended):**

```bash
# Unified interface
python scripts/orchestrator.py validate env
python scripts/orchestrator.py validate configs
```

**After (Direct - Alternative):**

```bash
# Direct execution with new paths
python scripts/python/validation/validate_env.py
python scripts/python/validation/validate_configs.py
```

### Example 2: Using Shared Utilities

**Before:**

```python
# validate_env.py (duplicated Colors class)
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

print(f"{Colors.GREEN}✓ Success{Colors.RESET}")
```

**After:**

```python
# Any Python script
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from python.utils.colors import success, error

print(success("Success"))  # Automatically colored
print(error("Failed"))
```

### Example 3: Running Code Quality Checks

**New Feature:**

```bash
# Via orchestrator
python scripts/orchestrator.py audit code

# Runs: Black, Ruff, mypy
# Output:
# === Running Black Format Check ===
# ✓ Black formatting check passed
#
# === Running Ruff Linter ===
# ✓ Ruff linting check passed
#
# === Running mypy Type Check ===
# ✓ mypy type check passed
```

---

## Troubleshooting

### Issue: "Module not found" errors

**Cause:** Python can't find the new package structure

**Solution:** Add parent directory to Python path:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

### Issue: "File not found" errors

**Cause:** Using old script paths

**Solution:** Update paths to new locations (see mapping table above)

### Issue: Import errors in Python scripts

**Cause:** Using old import patterns

**Solution:** Use package imports:

```python
# Old
from validate_env import Colors

# New
from python.utils.colors import Colors
```

### Issue: GitHub Actions failing

**Cause:** Workflow using old paths

**Solution:** Update workflow YAML:

```yaml
# Old
run: python scripts/validate_env.py

# New
run: python scripts/python/validation/validate_env.py
```

---

## Benefits of New Structure

### 1. Single Responsibility Principle (SRP)

- Each script has one clear purpose
- Easier to test and maintain
- Clearer dependencies

### 2. Don't Repeat Yourself (DRY)

- Shared utilities eliminate code duplication
- Consistent behavior across scripts
- Easier to update common functionality

### 3. Better Organization

- Scripts grouped by language and purpose
- Clear hierarchy and relationships
- Easier to navigate

### 4. Improved Documentation

- Module-specific README files
- Comprehensive examples
- Clear API documentation

### 5. Modern Python Standards

- Python 3.14 type hints
- PEP 585 built-in generics
- Enterprise-grade quality

---

## Support

For questions or issues:

1. Check module-specific README files in `scripts/python/*/README.md`
2. Review `scripts/README.md` for orchestrator usage
3. See `docs/python-setup-troubleshooting.md` for Python environment issues
4. Check git history for specific file migrations

---

## Timeline

- **v2.0.0**: Old flat structure
- **v3.0.0**: New organized structure (2025-10-25)
- **Migration Period**: N/A (clean break, no backward compatibility)

---

**Last Updated:** 2025-10-25  
**Migration Status:** Complete  
**Backward Compatibility:** None (use orchestrators or update paths)
