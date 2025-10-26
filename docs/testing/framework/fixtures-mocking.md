---
date_created: "2025-10-26T18:32:25.963815+00:00"
last_updated: "2025-10-26T18:32:25.963815+00:00"
tags: ['documentation', 'testing', 'pytest']
description: "Documentation for fixtures mocking"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- testing
- pytest
- mocking
- fixtures
description: Using pytest fixtures and mocking strategies
---\n# Fixtures and Mocking

Pytest fixtures and unittest.mock best practices.

## Fixtures

```python
import pytest

@pytest.fixture
def sample_data() -> dict[str, str]:
    """Provide sample test data."""
    return {"key": "value"}

def test_with_fixture(sample_data: dict[str, str]) -> None:
    """Test using fixture."""
    assert sample_data["key"] == "value"
```

## Mocking with unittest.mock

```python
from unittest.mock import Mock, patch

@patch('module.external_function')
def test_with_mock(mock_func: Mock) -> None:
    mock_func.return_value = "mocked"
    # Test code here
```

## Mock External Commands

```python
@patch('subprocess.run')
def test_subprocess(mock_run: Mock) -> None:
    mock_run.return_value = Mock(
        returncode=0,
        stdout="output"
    )
    # Test code that calls subprocess.run
```

## Mock File System

```python
import tempfile
from pathlib import Path

def test_file_operations() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("content")
        # Test file operations
```

## Shared Fixtures

Defined in `conftest.py`:
- `tmp_path`: Temporary directory
- `monkeypatch`: Modify environment
- `capsys`: Capture stdout/stderr
- Custom fixtures for project needs

## Mocking Guidelines

- Mock external dependencies (files, network, subprocess)
- Use `patch` decorator for function-level mocks
- Return Mock objects with specific attributes
- Verify mock calls with `assert_called_with`
