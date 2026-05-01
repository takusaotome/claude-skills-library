"""
Pytest configuration for action-status-updater tests.
"""

import sys
from pathlib import Path

# Add the scripts directory to the path for imports
scripts_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(scripts_dir))
