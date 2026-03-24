"""
pytest configuration for wbs-review-assistant tests
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import the scripts
scripts_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(scripts_dir))
