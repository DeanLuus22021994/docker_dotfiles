"""
Mock Redis operations for testing.

Provides in-memory Redis simulation for caching and session operations
to enable fast, isolated unit testing.
"""

from typing import Any, Dict, Optional
from unittest.mock import Mock


class RedisMock:
    """
    Mock Redis operations for testing.

    Provides in-memory Redis simulation for caching operations.
    """

    def __init__(self):
        self.data: dict[str, Any] = {}
        self.expire_times: dict[str, float] = {}

    def get(self, key: str) -> str | None:
        """Mock Redis GET."""
        if key in self.expire_times:
            import time
            if time.time() > self.expire_times[key]:
                del self.data[key]
                del self.expire_times[key]
                return None
        return self.data.get(key)

    def set(self, key: str, value: str, ex: int | None = None, **kwargs) -> bool:
        """Mock Redis SET with optional expiration."""
        self.data[key] = value
        if ex is not None:
            import time
            self.expire_times[key] = time.time() + ex
        return True

    def delete(self, key: str) -> int:
        """Mock Redis DELETE."""
        if key in self.data:
            del self.data[key]
            if key in self.expire_times:
                del self.expire_times[key]
            return 1
        return 0

    def exists(self, key: str) -> int:
        """Mock Redis EXISTS."""
        return 1 if key in self.data else 0

    def expire(self, key: str, time: int) -> int:
        """Mock Redis EXPIRE."""
        if key in self.data:
            import time as time_module
            self.expire_times[key] = time_module.time() + time
            return 1
        return 0

    def ttl(self, key: str) -> int:
        """Mock Redis TTL."""
        if key in self.expire_times:
            import time
            remaining = int(self.expire_times[key] - time.time())
            return remaining if remaining > 0 else -1
        return -1

    def keys(self, pattern: str = "*") -> list:
        """Mock Redis KEYS."""
        if pattern == "*":
            return list(self.data.keys())
        # Simple pattern matching for * wildcard
        return [k for k in self.data.keys() if pattern.replace("*", "") in k]

    def flushall(self) -> bool:
        """Mock Redis FLUSHALL."""
        self.data.clear()
        self.expire_times.clear()
        return True


class RedisClientMock:
    """
    Mock Redis client that behaves like redis.Redis().
    """

    def __init__(self, **kwargs):
        self.mock = RedisMock()

    def get(self, key: str) -> str | None:
        return self.mock.get(key)

    def set(self, key: str, value: str, ex: int | None = None, **kwargs) -> bool:
        return self.mock.set(key, value, ex, **kwargs)

    def delete(self, key: str) -> int:
        return self.mock.delete(key)

    def exists(self, key: str) -> int:
        return self.mock.exists(key)

    def expire(self, key: str, time: int) -> int:
        return self.mock.expire(key, time)

    def ttl(self, key: str) -> int:
        return self.mock.ttl(key)

    def keys(self, pattern: str = "*") -> list:
        return self.mock.keys(pattern)

    def flushall(self) -> bool:
        return self.mock.flushall()


# Global instances
redis_mock = RedisMock()
redis_client_mock = RedisClientMock()
