"""
Pytest configuration for meeting-asset-preparer tests.
"""

import sys
from pathlib import Path

# Add the scripts directory to the path for imports
scripts_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(scripts_dir))
