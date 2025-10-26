---
date_created: "2025-10-26T18:32:25.964335+00:00"
last_updated: "2025-10-26T18:32:25.964335+00:00"
tags: ["documentation", "testing", "pytest"]
description: "Documentation for overview"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- testing
- pytest
- overview
  description: Test suite structure and organization
  ---\n# Test Suite Overview

Comprehensive pytest-based test suite for Python modules.

## Directory Structure

```
tests/
├── conftest.py              # Shared fixtures
├── fixtures/                # Test data
└── python/
    ├── audit/              # Code quality tests
    │   ├── test_code_quality.py
    │   └── test_dependencies.py
    ├── utils/              # Utility tests
    │   ├── test_colors.py
    │   ├── test_file_utils.py
    │   └── test_logging_utils.py
    └── validation/         # Config validation tests
        ├── test_validate_env.py
        └── test_validate_configs.py
```

## Test Categories

**Unit Tests** (`@pytest.mark.unit`):

- Individual function/method isolation
- Mocked dependencies
- Fast execution (<1s)

**Integration Tests** (`@pytest.mark.integration`):

- Component interaction testing
- Real file system/subprocess
- Longer execution allowed

**Slow Tests** (`@pytest.mark.slow`):

- Tests taking >5 seconds
- Skip in development: `pytest -m "not slow"`

## Coverage Goals

- **Overall**: >80% (enforced)
- **Utils**: >90%
- **Validation**: >85%
- **Audit**: >85%

See subdocs for detailed testing guides.
