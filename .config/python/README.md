---
date_created: '2025-10-27T02:37:40Z'
last_updated: '2025-10-27T02:37:40Z'
tags: [python, pyright, pytest, configuration]
description: 'Python tooling configuration for type checking and testing'
---

# Python Configuration

Python tooling configuration for type checking, testing, and development.

## 📁 Files

### `pyrightconfig.json`
**Pyright type checker configuration**.

**Settings**:
- Python version: 3.14
- Type checking mode: basic
- Include: `scripts`, `tests`, `.config/mkdocs`
- Exclude: `__pycache__`, `node_modules`, `.venv`

**Features**:
- Import validation
- Type inference
- Module resolution

---

### `pytest.ini`
**Pytest testing configuration**.

**Settings**:
- Test discovery patterns
- Coverage reporting
- Markers for test categories

---

## 🚀 Quick Start

### Run Type Checking

```powershell
# Check all files
pyright

# Check specific file
pyright scripts/orchestrator.py
```

### Run Tests

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=scripts --cov-report=html
```

---

## 📚 References

- [Pyright Documentation](https://github.com/microsoft/pyright)
- [Pytest Documentation](https://docs.pytest.org/)
