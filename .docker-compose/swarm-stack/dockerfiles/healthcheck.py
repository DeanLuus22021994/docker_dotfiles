#!/usr/bin/env python3
"""
Health check script for swarm-stack Python service
Tests Python 3.14 features and Swarm connectivity
"""

import socket
import sys
from importlib.util import find_spec


def main() -> None:
    try:
        # Test Python 3.14 features
        if sys.version_info >= (3, 14) and find_spec("concurrent.interpreters"):
            print("Python 3.14 concurrent interpreters OK")
        else:
            print("Python version < 3.14 or interpreters not available")

        # Test Swarm connectivity (basic check)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("postgres", 5432))
        s.close()
        print("PostgreSQL connectivity OK")

        # Test Redis connectivity
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("redis", 6379))
        s.close()
        print("Redis connectivity OK")

        sys.exit(0)
    except Exception as e:
        print(f"Health check failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
