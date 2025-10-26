---
date_created: "2025-10-26T18:32:25.968101+00:00"
last_updated: "2025-10-26T18:32:25.968101+00:00"
tags: ["documentation", "testing", "pytest"]
description: "Documentation for pytest config"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- testing
- pytest
- configuration
- setup
  description: Pytest framework configuration and setup details
  ---\n# Pytest Configuration

## pyproject.toml Setup

**Dependencies:**

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.3",
    "pytest-cov>=6.0",
    "pytest-mock>=3.14",
    "pytest-asyncio>=0.24"
]
```

**Pytest Configuration:**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--strict-markers --cov-fail-under=80"
```

**Coverage Configuration:**

```toml
[tool.coverage.run]
source = ["scripts/python"]
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "if __name__ == .__main__.:"
]
```

## Additional Settings

Additional pytest configuration located in `.config/python/pytest.ini`:

- Async mode: `asyncio_mode = auto`
- Log level: DEBUG for test output
- Console output: short format

Root `pytest.ini` redirects to `.config/python/pytest.ini`.

## Installation

```bash
# Via UV (recommended)
uv pip install -e ".[dev]"

# Via pip
pip install -e ".[dev]"
```
