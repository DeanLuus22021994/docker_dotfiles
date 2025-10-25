# Test Suite Documentation

Comprehensive test suite for docker-modern-data-platform Python modules.

## Structure

```
tests/
├── conftest.py                      # Shared pytest fixtures
├── fixtures/                        # Test data and mock responses
├── python/
│   ├── audit/
│   │   ├── test_code_quality.py    # Black, Ruff, mypy tests
│   │   └── test_dependencies.py    # Package dependency tests
│   ├── utils/
│   │   ├── test_colors.py          # ANSI color utilities tests
│   │   ├── test_file_utils.py      # File I/O utilities tests
│   │   └── test_logging_utils.py   # Logging configuration tests
│   └── validation/
│       ├── test_validate_env.py    # Environment validation tests
│       └── test_validate_configs.py # Config file validation tests
```

## Running Tests

### Run All Tests

```bash
# Run all tests with coverage
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=scripts/python --cov-report=html
```

### Run Specific Test Modules

```bash
# Run utils tests only
pytest tests/python/utils/

# Run validation tests only
pytest tests/python/validation/

# Run audit tests only
pytest tests/python/audit/

# Run specific test file
pytest tests/python/utils/test_colors.py

# Run specific test class
pytest tests/python/utils/test_colors.py::TestColorize

# Run specific test function
pytest tests/python/utils/test_colors.py::TestColorize::test_colorize_basic
```

### Run Tests by Marker

```bash
# Run unit tests only
pytest -m unit

# Run integration tests only
pytest -m integration

# Run all except slow tests
pytest -m "not slow"
```

## Test Coverage

### Coverage Goals

- **Overall**: >80% coverage (enforced)
- **Utils Module**: >90% coverage
- **Validation Module**: >85% coverage
- **Audit Module**: >85% coverage

### Generate Coverage Report

```bash
# Terminal report with missing lines
pytest --cov=scripts/python --cov-report=term-missing

# HTML report (opens in browser)
pytest --cov=scripts/python --cov-report=html
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows

# XML report (for CI/CD)
pytest --cov=scripts/python --cov-report=xml
```

## Writing Tests

### Test Naming Conventions

- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<functionality>_<scenario>`

### Example Test Structure

```python
"""Tests for example_module."""

import pytest
from python.module import function_to_test


class TestFunctionName:
    """Test function_to_test function."""

    def test_basic_functionality(self) -> None:
        """Test basic use case."""
        result = function_to_test("input")
        assert result == "expected"

    def test_edge_case(self) -> None:
        """Test edge case handling."""
        with pytest.raises(ValueError):
            function_to_test(None)

    @pytest.mark.parametrize("input,expected", [
        ("a", "result_a"),
        ("b", "result_b"),
    ])
    def test_multiple_inputs(self, input: str, expected: str) -> None:
        """Test multiple inputs."""
        assert function_to_test(input) == expected
```

### Using Fixtures

```python
@pytest.fixture
def sample_data() -> dict[str, str]:
    """Provide sample test data."""
    return {"key": "value"}


def test_with_fixture(sample_data: dict[str, str]) -> None:
    """Test using fixture."""
    assert sample_data["key"] == "value"
```

## Test Categories

### Unit Tests

- Test individual functions/methods in isolation
- Mock external dependencies
- Fast execution (<1s per test)
- Mark with `@pytest.mark.unit`

### Integration Tests

- Test interaction between components
- May use real file system/subprocess
- Longer execution time allowed
- Mark with `@pytest.mark.integration`

### Slow Tests

- Tests that take >5 seconds
- Mark with `@pytest.mark.slow`
- Skip in regular development: `pytest -m "not slow"`

## Mocking Guidelines

### Use unittest.mock

```python
from unittest.mock import Mock, patch

@patch('module.external_function')
def test_with_mock(mock_func: Mock) -> None:
    mock_func.return_value = "mocked"
    # Test code here
```

### Mock External Commands

```python
@patch('subprocess.run')
def test_subprocess(mock_run: Mock) -> None:
    mock_run.return_value = Mock(returncode=0, stdout="output")
    # Test code that calls subprocess.run
```

### Mock File System

```python
import tempfile
from pathlib import Path

def test_file_operations() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        # Test file operations
```

## Continuous Integration

Tests are automatically run on:

- Every push to main branch
- Every pull request
- Scheduled nightly builds

See `.github/workflows/test.yml` for CI configuration.

## Troubleshooting

### Import Errors

If you see import errors like `Import "python.module" could not be resolved`:

1. Ensure you're running from project root
2. Check that `conftest.py` adds scripts to path
3. Verify Python path: `python -c "import sys; print(sys.path)"`

### Coverage Not Meeting Threshold

```bash
# See which lines are missing coverage
pytest --cov=scripts/python --cov-report=term-missing

# Generate HTML report for detailed view
pytest --cov=scripts/python --cov-report=html
```

### Slow Test Suite

```bash
# Skip slow tests during development
pytest -m "not slow"

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

## Best Practices

1. **One assertion per test** (when possible)
2. **Clear test names** describing what is tested
3. **Arrange-Act-Assert** pattern
4. **Mock external dependencies** (files, network, subprocess)
5. **Use parametrize** for testing multiple inputs
6. **Test edge cases** (None, empty, very large values)
7. **Test error handling** (exceptions, invalid input)
8. **Keep tests fast** (<100ms per unit test)
9. **Independent tests** (no shared state)
10. **Meaningful assertions** (not just `assert True`)

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Python testing best practices](https://realpython.com/pytest-python-testing/)
