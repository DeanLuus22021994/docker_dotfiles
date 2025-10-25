# Audit Module

Python scripts for automated code quality auditing and dependency management.

## Overview

The audit module provides comprehensive tools for maintaining code quality standards and tracking package dependencies. All checks can be run individually or through the orchestrator.

## Scripts

### code_quality.py

**Purpose:** Run automated code quality checks across the entire codebase

**Usage:**

```powershell
# Via orchestrator (recommended)
python ../orchestrator.py audit code

# Direct execution
python code_quality.py
```

**Checks Performed:**

- **Black**: Code formatting (line-length=100)
- **Ruff**: Fast Python linter (replaces Flake8, isort, etc.)
- **mypy**: Static type checking with strict mode

**Exit Codes:**

- `0` = All checks passed
- `1` = One or more checks failed

**Example Output:**

```
=== Running Black Format Check ===
✓ Black formatting check passed

=== Running Ruff Linter ===
✓ Ruff linting check passed

=== Running mypy Type Check ===
✓ mypy type check passed

✓ ALL CODE QUALITY CHECKS PASSED
```

**Configuration:**

- Black: `pyproject.toml` (line-length = 100)
- Ruff: `pyproject.toml` (strict linting rules)
- mypy: `pyproject.toml` (strict mode enabled)

---

### dependencies.py

**Purpose:** Check for outdated packages and validate dependencies

**Usage:**

```powershell
# Via orchestrator (recommended)
python ../orchestrator.py audit deps

# Direct execution
python dependencies.py
```

**Checks Performed:**

- **Outdated Packages**: Uses `pip list --outdated` to find packages with newer versions
- **Required Dependencies**: Validates all packages in `pyproject.toml` are installed
- **Installed Packages**: Lists all packages with their current versions

**Exit Codes:**

- `0` = All checks passed
- `1` = Outdated packages or missing dependencies found

**Example Output:**

```
=== Checking Outdated Packages ===
⚠ Found 3 outdated packages:
  - package1: 1.0.0 → 2.0.0 (latest)
  - package2: 3.1.0 → 3.2.0 (latest)

=== Checking pyproject.toml Dependencies ===
✓ All required packages are installed

=== Installed Packages ===
ℹ Total packages: 42
  - black==24.10.0
  - ruff==0.7.0
  - mypy==1.13.0
  ...
```

---

## Module API

### Import Patterns

```python
# Import specific modules
from python.audit import code_quality, dependencies

# Import all (via __all__)
from python.audit import *

# Import specific functions
from python.audit.code_quality import run_black_check, run_ruff_check
from python.audit.dependencies import check_outdated_packages
```

### Exports

The module exports the following via `__all__`:

- `code_quality` - Code quality checking module
- `dependencies` - Dependency auditing module

---

## Type Annotations

All functions use modern Python 3.14 type hints:

```python
def run_black_check() -> tuple[bool, list[str]]:
    """Run Black formatter in check mode."""
    errors: list[str] = []
    # ...
    return success, errors

def check_outdated_packages() -> tuple[bool, list[str]]:
    """Check for outdated Python packages."""
    errors: list[str] = []
    # ...
    return success, errors
```

---

## Dependencies

**Required:**

- `black` - Code formatter
- `ruff` - Fast Python linter
- `mypy` - Static type checker
- `pip` - Package management (included with Python)

**Installation:**

```powershell
# Using UV (recommended)
uv pip install black ruff mypy

# Using pip
pip install black ruff mypy
```

---

## Integration with Orchestrator

The orchestrator provides convenient access to all audit scripts:

```powershell
# PowerShell
..\orchestrator.ps1 audit code
..\orchestrator.ps1 audit deps

# Bash
../orchestrator.sh audit code
../orchestrator.sh audit deps

# Python
python ..\orchestrator.py audit code
python ..\orchestrator.py audit deps
```

---

## Best Practices

### Running Before Commits

```powershell
# Check code quality
python ../orchestrator.py audit code

# Check dependencies
python ../orchestrator.py audit deps

# If all pass, commit
git add .
git commit -m "Your message"
```

### CI/CD Integration

Add to your CI pipeline:

```yaml
# GitHub Actions example
- name: Audit Code Quality
  run: python scripts/orchestrator.py audit code

- name: Audit Dependencies
  run: python scripts/orchestrator.py audit deps
```

### Pre-commit Hooks

Configure in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: audit-code
        name: Audit Code Quality
        entry: python scripts/orchestrator.py audit code
        language: system
        pass_filenames: false
```

---

## Standards Compliance

### Python 3.14

- ✅ PEP 585: Built-in generics (`list[str]`, `tuple[bool, list[str]]`)
- ✅ PEP 649: Deferred annotation evaluation
- ✅ PEP 484: Type hints on all functions

### Code Quality

- ✅ Black formatting (line-length=100)
- ✅ Ruff linting (strict mode)
- ✅ mypy type checking (strict mode)
- ✅ Zero suppressions or ignores

---

## Troubleshooting

### "Module not found" errors

Ensure parent directory is in Python path:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

### Black/Ruff/mypy not found

Install required tools:

```powershell
uv pip install black ruff mypy
```

### Permission errors

Run with appropriate privileges or check file permissions.

---

**Last Updated:** 2025-10-25  
**Python Version:** 3.14.0+  
**Module Version:** 1.0.0
