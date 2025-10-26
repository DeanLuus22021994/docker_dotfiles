---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["testing", "fixtures", "sample-data", "pytest"]
description: "Shared test fixtures and sample data for test suites"
---

# Test fixtures and sample data

This directory contains shared test fixtures and sample data used across test suites.

## Structure

- `sample_configs/` - Sample configuration files for testing
- `sample_data/` - Sample data files (JSON, CSV, etc.)
- `mock_responses/` - Mock API responses

## Usage

Import fixtures in tests using:

```python
from pathlib import Path
import pytest

@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent / "fixtures"
```
