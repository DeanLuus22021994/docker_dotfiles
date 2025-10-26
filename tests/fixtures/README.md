---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["testing", "fixtures", "sample-data", "pytest"]
description: "Shared test fixtures and sample data for test suites"
---

# Test Fixtures

Centralized test fixtures providing standardized test infrastructure across all test modules.

## Structure

```
tests/fixtures/
├── __init__.py          # Package initialization with exports
├── common.py            # Core fixture implementations
├── README.md            # This file
├── sample_configs/      # Sample configuration files
├── sample_data/         # Sample data files (JSON, CSV, etc.)
└── mock_responses/      # Mock API responses
```

## Available Fixtures

All fixtures are **automatically available** in all test modules via `conftest.py` registration. No explicit imports needed.

### Temporary File System Fixtures

#### `temp_dir`

Creates temporary directory, automatically cleaned up after test.

```python
def test_file_creation(temp_dir: Path) -> None:
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")
    assert test_file.exists()
```

#### `temp_project_dir`

Creates temporary project with `.config/nginx/` and `.config/database/` structure.

```python
def test_config(temp_project_dir: Path) -> None:
    nginx_conf = temp_project_dir / ".config" / "nginx" / "main.conf"
    nginx_conf.write_text("server { }")
```

#### `sample_json_file`

Pre-created JSON file with test data:

```json
{ "name": "test", "value": 42, "items": ["a", "b", "c"] }
```

```python
def test_read_json(sample_json_file: Path) -> None:
    data = json.loads(sample_json_file.read_text())
    assert data["name"] == "test"
```

#### `sample_text_file`

Pre-created text file with three lines: "line1", "line2", "line3"

```python
def test_read_lines(sample_text_file: Path) -> None:
    lines = sample_text_file.read_text().splitlines()
    assert len(lines) == 3
```

### Environment Variable Fixtures

#### `clean_env`

Clears and restores all Docker/GitHub environment variables:

- `GITHUB_OWNER`, `GH_PAT`
- `DOCKER_POSTGRES_PASSWORD`, `DOCKER_MARIADB_ROOT_PASSWORD`, etc.
- `DOCKER_ACCESS_TOKEN`, `CODECOV_TOKEN`

```python
def test_env_validation(clean_env: None) -> None:
    os.environ["GH_PAT"] = "test_token"
    # Test environment validation
    # Original values automatically restored after test
```

### Logger Cleanup Fixtures

#### `cleanup_loggers`

Clears all logger handlers and resets log levels after each test.

```python
def test_logging(cleanup_loggers: None) -> None:
    logger = logging.getLogger("test")
    logger.info("test message")
    # Logger automatically cleaned up after test
```

## Usage Patterns

### Basic Test with Fixture

```python
def test_something(temp_dir: Path) -> None:
    """No import needed - fixture auto-injected."""
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")
    assert test_file.read_text() == "content"
```

### Multiple Fixtures

```python
def test_complex(temp_dir: Path, clean_env: None) -> None:
    """Use multiple fixtures together."""
    os.environ["TEST_VAR"] = "value"
    config_file = temp_dir / "config.json"
    config_file.write_text('{"key": "value"}')
```

### Fixture Composition

```python
# temp_project_dir depends on temp_dir
def test_project_structure(temp_project_dir: Path) -> None:
    nginx_dir = temp_project_dir / ".config" / "nginx"
    assert nginx_dir.exists()
```

## Separation of Concerns

### Before (Duplicated Fixtures)

```python
# test_file_utils.py
@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

# test_logging_utils.py
@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
```

### After (Centralized)

```python
# tests/fixtures/common.py
@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Single source of truth for temp directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

# All tests automatically have access
def test_something(temp_dir: Path) -> None:
    # Works in any test file
    pass
```

## Benefits

✅ **Zero Duplication** - Single fixture definition used across all tests
✅ **Standardization** - Consistent test infrastructure everywhere
✅ **Automatic Cleanup** - All fixtures handle resource cleanup
✅ **Type Safety** - Full type hints for IDE support
✅ **Documentation** - Comprehensive docstrings with examples
✅ **Separation of Concerns** - Test logic separated from test infrastructure

## Adding New Fixtures

1. Add fixture to `tests/fixtures/common.py` with full docstring
2. Export fixture name in `tests/fixtures/__init__.py`
3. Fixture automatically available in all tests

```python
# tests/fixtures/common.py
@pytest.fixture
def my_fixture() -> str:
    """Description and usage example."""
    return "fixture_value"

# tests/fixtures/__init__.py
__all__ = [..., "my_fixture"]

# tests/python/test_something.py
def test_something(my_fixture: str) -> None:
    assert my_fixture == "fixture_value"
```

## Architecture

```
┌─────────────────────────────────────────┐
│ conftest.py                             │
│ ├── sys.path setup                      │
│ └── pytest_plugins = ["fixtures.common"]│
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ fixtures/common.py                      │
│ ├── temp_dir                            │
│ ├── temp_project_dir                    │
│ ├── sample_json_file                    │
│ ├── sample_text_file                    │
│ ├── clean_env                           │
│ └── cleanup_loggers                     │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ All Test Modules (Auto-Injected)       │
│ ├── test_file_utils.py                 │
│ ├── test_logging_utils.py              │
│ ├── test_validate_env.py               │
│ ├── test_validate_configs.py           │
│ └── ...                                 │
└─────────────────────────────────────────┘
```
