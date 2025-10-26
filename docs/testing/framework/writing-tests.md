---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["testing", "pytest", "writing-tests", "best-practices"]
description: "Guidelines for writing effective pytest tests"
---
# Writing Tests

Best practices and conventions for pytest tests.

## Naming Conventions

- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<functionality>_<scenario>`

## Test Structure

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

## Best Practices

1. **One assertion per test** (when possible)
2. **Clear test names** describing what is tested
3. **Arrange-Act-Assert** pattern
4. **Mock external dependencies**
5. **Use parametrize** for multiple inputs
6. **Test edge cases** (None, empty, large values)
7. **Test error handling**
8. **Keep tests fast** (<100ms per unit test)
9. **Independent tests** (no shared state)
10. **Meaningful assertions**
