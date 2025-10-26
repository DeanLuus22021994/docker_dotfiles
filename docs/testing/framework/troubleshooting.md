---
date_created: "2025-10-26T18:32:25.965751+00:00"
last_updated: "2025-10-26T18:32:25.965751+00:00"
tags: ["documentation", "testing", "pytest"]
description: "Documentation for troubleshooting"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- testing
- troubleshooting
- debugging
  description: Common testing issues and solutions
  ---\n# Testing Troubleshooting

Solutions for common pytest issues.

## Import Errors

**Issue:** `Import "python.module" could not be resolved`

**Solutions:**

1. Run from project root directory
2. Check `conftest.py` adds scripts to path
3. Verify Python path:

```bash
python -c "import sys; print(sys.path)"
```

## Coverage Not Meeting Threshold

**Issue:** Tests fail due to <80% coverage

**Solutions:**

```bash
# See missing lines
pytest --cov=scripts/python --cov-report=term-missing

# HTML report for details
pytest --cov=scripts/python --cov-report=html
start htmlcov/index.html  # Windows
```

## Slow Test Suite

**Issue:** Tests take too long during development

**Solutions:**

```bash
# Skip slow tests
pytest -m "not slow"

# Run in parallel (requires pytest-xdist)
pytest -n auto

# Run specific module only
pytest tests/python/utils/
```

## Fixture Not Found

**Issue:** `fixture 'name' not found`

**Solutions:**

1. Check fixture is defined in `conftest.py`
2. Verify fixture scope matches test scope
3. Import fixture if defined in another module

## Mock Not Working

**Issue:** Mock not intercepting calls

**Solutions:**

1. Patch the correct import path (where it's used, not where it's defined)
2. Use `@patch` decorator above function
3. Verify mock is applied before function call

## Test Isolation Issues

**Issue:** Tests fail when run together but pass individually

**Solutions:**

1. Use fixtures with proper scope (`function`, not `module`)
2. Clean up side effects in teardown
3. Avoid global state modifications
4. Use `monkeypatch` for environment variables
