"""Path Setup Module - imported first to configure sys.path.

This module MUST be imported before any other local modules.
It adds the scripts directory to sys.path to enable imports.
"""

import sys
from pathlib import Path

# Get scripts directory (parent of python/)
SCRIPTS_DIR = Path(__file__).parent.parent

# Add to sys.path if not already present
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
