"""
Pytest configuration for multi-file-log-correlator tests.
"""

import sys
from pathlib import Path

# Add the scripts directory to the Python path
scripts_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(scripts_dir))
