"""
Pytest configuration for meeting-minutes-reviewer tests.
"""

import sys
from pathlib import Path

# Add scripts directory to path for imports
scripts_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(scripts_dir))
