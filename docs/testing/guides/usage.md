---
date_created: "2025-10-26T18:32:25.969313+00:00"
last_updated: "2025-10-26T18:32:25.969313+00:00"
tags: ['documentation', 'testing', 'pytest']
description: "Documentation for usage"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- testing
- usage
- commands
- coverage
description: Testing commands and usage examples
---\n# Testing Usage Guide

## Run All Tests

```bash
# Basic run
pytest

# With verbose output
pytest -v

# With coverage
pytest --cov=scripts/python --cov-report=html
```

## Run Specific Tests

```bash
# Single module
pytest tests/python/utils/

# Single file
pytest tests/python/utils/test_colors.py

# Single test function
pytest tests/python/utils/test_colors.py::test_color_codes

# Pattern matching
pytest -k "color"
```

## Coverage Reports

```bash
# HTML report
pytest --cov=scripts/python --cov-report=html
# Open: htmlcov/index.html

# Terminal report
pytest --cov=scripts/python --cov-report=term

# XML for CI/CD
pytest --cov=scripts/python --cov-report=xml
```

## Debugging

```bash
# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Show locals on failure
pytest -l

# PDB on failure
pytest --pdb
```

## Parallel Execution

```bash
# Install plugin
pip install pytest-xdist

# Run with 4 workers
pytest -n 4
```

## Watch Mode

```bash
# Install plugin
pip install pytest-watch

# Auto-run on changes
ptw
```
