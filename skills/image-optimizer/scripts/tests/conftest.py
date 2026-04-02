"""
Pytest configuration for image-optimizer tests.
"""

import sys
from pathlib import Path

# Add scripts directory to Python path for imports
scripts_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))
