---
date_created: "2025-10-26T18:32:25.965101+00:00"
last_updated: "2025-10-26T18:32:25.965101+00:00"
tags: ["documentation", "testing", "pytest"]
description: "Documentation for running tests"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- testing
- pytest
- commands
  description: Running tests with pytest
  ---\n# Running Tests

Execute pytest tests with various configurations and filters.

## Basic Commands

```bash
# Run all tests with coverage
pytest

# Verbose output
pytest -v

# Coverage report (HTML)
pytest --cov=scripts/python --cov-report=html
```

## Specific Test Execution

```bash
# Run single module
pytest tests/python/utils/

# Run single file
pytest tests/python/utils/test_colors.py

# Run single class
pytest tests/python/utils/test_colors.py::TestColorize

# Run single test
pytest tests/python/utils/test_colors.py::TestColorize::test_colorize_basic
```

## Filter by Marker

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Coverage Reports

```bash
# Terminal with missing lines
pytest --cov=scripts/python --cov-report=term-missing

# HTML report (open in browser)
pytest --cov=scripts/python --cov-report=html
start htmlcov/index.html  # Windows

# XML report (for CI/CD)
pytest --cov=scripts/python --cov-report=xml
```

## Parallel Execution

```bash
# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```
