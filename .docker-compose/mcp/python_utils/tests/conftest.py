"""
Pytest configuration and fixtures for Docker Compose Utils tests.

Provides test configuration for isolated testing.
"""

import sys
from pathlib import Path

# Add tests directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent))
